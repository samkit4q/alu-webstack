import os

class SparseMatrix:
    def __init__(self, file_path=None, num_rows=0, num_cols=0):
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.elements = {}
        if file_path:
            self._load_from_file(file_path)

    def _load_from_file(self, file_path):
        with open(file_path, 'r') as file:
            lines = file.readlines()
            self.num_rows = int(lines[0].split('=')[1].strip())
            self.num_cols = int(lines[1].split('=')[1].strip())
            for line in lines[2:]:
                if line.strip():
                    try:
                        row, col, value = self._parse_entry(line)
                        self.set_element(row, col, value)
                    except ValueError:
                        raise ValueError("Input file has wrong format")

    def _parse_entry(self, line):
        line = line.strip()
        if not (line.startswith('(') and line.endswith(')')):
            raise ValueError("Input file has wrong format")
        parts = line[1:-1].split(',')
        if len(parts) != 3:
            raise ValueError("Input file has wrong format")
        row = int(parts[0].strip())
        col = int(parts[1].strip())
        value = int(parts[2].strip())
        return row, col, value

    def get_element(self, row, col):
        return self.elements.get((row, col), 0)

    def set_element(self, row, col, value):
        if value != 0:
            self.elements[(row, col)] = value
        elif (row, col) in self.elements:
            del self.elements[(row, col)]

    def __str__(self):
        elements = [f"({r}, {c}, {v})" for (r, c), v in self.elements.items()]
        return f"Rows: {self.num_rows}, Cols: {self.num_cols}, Elements: {elements}"

def add_matrices(matrix1, matrix2):
    if matrix1.num_rows != matrix2.num_rows or matrix1.num_cols != matrix2.num_cols:
        raise ValueError("Matrices dimensions must match for addition")

    result = SparseMatrix(num_rows=matrix1.num_rows, num_cols=matrix1.num_cols)
    for key in set(matrix1.elements.keys()).union(matrix2.elements.keys()):
        result.set_element(*key, matrix1.get_element(*key) + matrix2.get_element(*key))
    return result

def subtract_matrices(matrix1, matrix2):
    if matrix1.num_rows != matrix2.num_rows or matrix1.num_cols != matrix2.num_cols:
        raise ValueError("Matrices dimensions must match for subtraction")

    result = SparseMatrix(num_rows=matrix1.num_rows, num_cols=matrix1.num_cols)
    for key in set(matrix1.elements.keys()).union(matrix2.elements.keys()):
        result.set_element(*key, matrix1.get_element(*key) - matrix2.get_element(*key))
    return result

def multiply_matrices(matrix1, matrix2):
    if matrix1.num_cols != matrix2.num_rows:
        raise ValueError("Number of columns in the first matrix must be equal to the number of rows in the second matrix")

    result = SparseMatrix(num_rows=matrix1.num_rows, num_cols=matrix2.num_cols)
    for (i, k), value1 in matrix1.elements.items():
        for j in range(matrix2.num_cols):
            value2 = matrix2.get_element(k, j)
            if value2 != 0:
                result.set_element(i, j, result.get_element(i, j) + value1 * value2)
    return result

def main():
    base_dir = '/dsa/sparse_matrix/sample_inputs/'
    file1 = os.path.join(base_dir, 'matrix1.txt')
    file2 = os.path.join(base_dir, 'matrix2.txt')

    matrix1 = SparseMatrix(file_path=file1)
    matrix2 = SparseMatrix(file_path=file2)

    print("Choose operation: 1. Addition 2. Subtraction 3. Multiplication")
    choice = int(input().strip())

    if choice == 1:
        result = add_matrices(matrix1, matrix2)
    elif choice == 2:
        result = subtract_matrices(matrix1, matrix2)
    elif choice == 3:
        result = multiply_matrices(matrix1, matrix2)
    else:
        print("Invalid choice")
        return

    print(result)

if __name__ == "__main__":
    main()


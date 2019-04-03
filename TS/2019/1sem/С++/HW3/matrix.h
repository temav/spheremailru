class Matrix
{
	int* Mat;
	const size_t Size, Rows, Columns;
	class Matrix_Row
	{
		size_t size_R;
		int* Mat_R; 
	public:
		Matrix_Row(int* a, size_t b) : Mat_R(a), size_R(b)
		{}
		const int& operator [] (size_t index_row) const
		{
			if (index_row >= size_R)
				throw std::out_of_range("");
			return Mat_R[index_row];
		}
		int& operator [] (size_t index_row)
		{
			if (index_row >= size_R)
				throw std::out_of_range("");
			return Mat_R[index_row];
		}
	};
public:
	Matrix(size_t str, size_t col) : Rows(str), Columns(col), Size(str * col)
	{
		Mat = new int [Size];
	}
	const Matrix_Row operator [] (size_t index_row) const
	{
		if(index_row >= Rows)
			throw std::out_of_range("");
		return Matrix_Row(Mat + index_row * Columns, Columns);
	}
	Matrix_Row operator [] (size_t index_row)
	{
		if(index_row >= Rows)
			throw std::out_of_range("");
	 	return Matrix_Row(Mat + index_row * Columns, Columns);
	}
        Matrix& operator *= (int Mul)
        {
	        for (int i = 0; i < Size; ++i)
			Mat[i] *= Mul;
		return *this;
 	}
        bool operator == (const Matrix& other)
        {
	        if ((Rows != other.getRows()) || (Columns != other.getColumns())) 
	        	return 0;
		for (int i = 0; i < Size; ++i)
		{
			if (Mat[i] != other.Mat[i])
				return 0;
		}
		return 1;
	}
	bool operator != (const Matrix& other)
	{
		return !(*this == other);
	}
	size_t getRows() const
	{
		return Rows;
	}
	size_t getColumns() const
	{
		return Columns;
	}
	~Matrix()
	{
		delete[] Mat;
	}
};

from lib import CONN, CURSOR

class Review:
    def __init__(self, year, summary, employee_id=None):
        self.id = None  # Default value
        self.year = year
        self.summary = summary
        self.employee_id = employee_id

    def __repr__(self):
        return f"<Review id={self.id}, year={self.year}, summary='{self.summary}', employee_id={self.employee_id}>"

    @classmethod
    def create_table(cls):
        CURSOR.execute('''
            CREATE TABLE IF NOT EXISTS reviews (
                id INTEGER PRIMARY KEY,
                year INTEGER NOT NULL,
                summary TEXT NOT NULL,
                employee_id INTEGER,
                FOREIGN KEY (employee_id) REFERENCES employees (id)
            )
        ''')
        CONN.commit()

    @classmethod
    def drop_table(cls):
        CURSOR.execute('DROP TABLE IF EXISTS reviews')
        CONN.commit()

    def save(self):
        CURSOR.execute('''
            INSERT INTO reviews (year, summary, employee_id) VALUES (?, ?, ?)
        ''', (self.year, self.summary, self.employee_id))
        self.id = CURSOR.lastrowid  # Update object id
        CONN.commit()

    @classmethod
    def create(cls, year, summary, employee_id):
        review = cls(year, summary, employee_id)
        review.save()  # Save using the instance method
        return review

    @classmethod
    def instance_from_db(cls, row):
        if row[0] in cls.all_reviews:  # row[0] is the id
            return cls.all_reviews[row[0]]
        review = cls(row[1], row[2], row[3])  # Create from row
        review.id = row[0]  # Set id
        cls.all_reviews[row[0]] = review  # Cache the instance
        return review

    @classmethod
    def find_by_id(cls, review_id):
        CURSOR.execute('SELECT * FROM reviews WHERE id = ?', (review_id,))
        row = CURSOR.fetchone()
        return cls.instance_from_db(row) if row else None

    def update(self, year, summary, employee_id):
        self.year = year
        self.summary = summary
        self.employee_id = employee_id
        CURSOR.execute('''
            UPDATE reviews SET year = ?, summary = ?, employee_id = ? WHERE id = ?
        ''', (self.year, self.summary, self.employee_id, self.id))
        CONN.commit()

    def delete(self):
        CURSOR.execute('DELETE FROM reviews WHERE id = ?', (self.id,))
        CONN.commit()
        del self.all_reviews[self.id]  # Remove from cache
        self.id = None  # Reset id

    @classmethod
    def get_all(cls):
        CURSOR.execute('SELECT * FROM reviews')
        rows = CURSOR.fetchall()
        return [cls.instance_from_db(row) for row in rows]

# Initialize a cache for all reviews
Review.all_reviews = {}

class Review:
    # ... [existing methods]

    @property
    def year(self):
        return self._year

    @year.setter
    def year(self, value):
        if not isinstance(value, int) or value < 2000:
            raise ValueError("Year must be an integer greater than or equal to 2000.")
        self._year = value

    @property
    def summary(self):
        return self._summary

    @summary.setter
    def summary(self, value):
        if not value or not isinstance(value, str):
            raise ValueError("Summary must be a non-empty string.")
        self._summary = value

    @property
    def employee_id(self):
        return self._employee_id

    @employee_id.setter
    def employee_id(self, value):
        if not isinstance(value, int):
            raise ValueError("Employee ID must be an integer.")
        self._employee_id = value

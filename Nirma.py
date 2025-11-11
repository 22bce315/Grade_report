import pandas as pd
import numpy as np

class GradePredictor:
    def __init__(self):
        self.data = []   
        self.df = pd.DataFrame()
    def add(self, subjects="", ct=0, sessional=0, assignment=0, index=0, practical=0, has_lpw=0):
        self.data.append({
            'subjects': subjects,
            'ct': ct,
            'sessional': sessional,
            'assignment': assignment,
            'index': index,
            'practical': practical,
            'has_lpw': bool(has_lpw)
        })
    def add_batch(self, dict_list):
        """
        Expects a list of dictionaries like:
        ```pyton 
        [
         {
          'subjects': 'PCD', 
          'ct': 16, 
          'sessional': 42, 
          'assignment': 16, 
          'index': 89, 
          'practical': 37, 
          'has_lpw': 1
          }, 
          ...
        ]
        ```
        """
        for d in dict_list:
            d.setdefault('subjects', "")
            d.setdefault('ct', 0)
            d.setdefault('sessional', 0)
            d.setdefault('assignment', 0)
            d.setdefault('index', 0)
            d.setdefault('practical', 0)
            d.setdefault('has_lpw', 0)
            d['has_lpw'] = bool(d['has_lpw'])
            self.data.append(d)
    def add_input(self):
        print("Enter details for a subject:")
        subjects = input("Subject name: ")
        ct = float(input("CT marks: ") or 0)
        sessional = float(input("Sessional marks: ") or 0)
        assignment = float(input("Assignment marks: ") or 0)
        index = float(input("Index marks: ") or 0)
        practical = float(input("Practical marks: ") or 0)
        has_lpw = bool(int(input("Has LPW? (1/0): ") or 0))
        self.add(subjects, ct, sessional, assignment, index, practical, has_lpw)
    def fit(self, dict_list=None):
      if dict_list:
         self.add_batch(dict_list)
      if not self.data:
         print("No data to fit. Please add subjects first.")
         return

      df = pd.DataFrame(self.data)
      df['CE'] = np.where(
         df['has_lpw'],
         df['ct'] + df['assignment'] + df['sessional'] * 6/5,
         df['ct'] * 3/2 + df['assignment'] + df['sessional'] * 4/5
      )
      df['LPW'] = np.where(df['has_lpw'], df['index'] * 6/10 + df['practical'], 0)
      df['CE_C'] = np.ceil(df['CE'])
      df['LPW_C'] = np.ceil(df['LPW'])

      grade_thresholds = {
         'C': 50.1, 'C+': 60.1, 'B': 65.1, 'B+': 67.6,
         'A': 70.1, 'A+': 80.1, 'O': 90.1
      }

      for grade, target in grade_thresholds.items():
         df[f'{grade}'] = 0
         df[f'{grade}_C'] = 0
         for i, row in df.iterrows():
               if row['has_lpw']:
                  df.loc[i, grade] = np.ceil((target - (0.3 * row['CE'] + 0.3 * row['LPW'])) / 0.4)
                  df.loc[i, f'{grade}_C'] = np.ceil((target - (0.3 * row['CE_C'] + 0.3 * row['LPW_C'])) / 0.4)
               else:
                  df.loc[i, grade] = np.ceil((target - (0.6 * row['CE'])) / 0.4)
                  df.loc[i, f'{grade}_C'] = np.ceil((target - (0.6 * row['CE_C'])) / 0.4)

      grade_cols = [col for col in df.columns if any(g in col for g in grade_thresholds.keys())]
      df[grade_cols] = df[grade_cols].astype(int)
      self.df = df

    def show_df(self):
        if self.df.empty:
            print("Data not fitted yet. Run fit() first.")
            return None
        return self.df
    def show_endsem_prediction(self, from_grade='C', till_grade='O'):
      """
      Shows grade predictions between 'from_grade' and 'till_grade' inclusive.
      
      Parameters:
         from_grade: starting grade level (default 'C')
         till_grade: ending grade level (default 'O')

      Valid grade order:
         C, C+, B, B+, A, A+, O
      """
      if self.df.empty:
         print("Data not fitted yet. Run fit() first.")
         return None

      all_grades = ['C', 'C+', 'B', 'B+', 'A', 'A+', 'O']

      if from_grade not in all_grades or till_grade not in all_grades:
         print("Invalid grade range. Choose from:", all_grades)
         return None

      start_idx = all_grades.index(from_grade)
      end_idx = all_grades.index(till_grade)

      if start_idx > end_idx:
         print("Invalid range: from_grade should be lower than till_grade.")
         return None

      selected_grades = all_grades[start_idx:end_idx + 1]
      cols = ['subjects'] + [g for grade in selected_grades for g in [grade, f'{grade}_C']]
      return self.df[cols]
    
    def predict(self, from_grade='C', till_grade='O'):
      """
      Shows grade predictions between 'from_grade' and 'till_grade' inclusive.
      
      Parameters:
         from_grade: starting grade level (default 'C')
         till_grade: ending grade level (default 'O')

      Valid grade order:
         C, C+, B, B+, A, A+, O
      """
      if self.df.empty:
         print("Data not fitted yet. Run fit() first.")
         return None

      all_grades = ['C', 'C+', 'B', 'B+', 'A', 'A+', 'O']

      if from_grade not in all_grades or till_grade not in all_grades:
         print("Invalid grade range. Choose from:", all_grades)
         return None

      start_idx = all_grades.index(from_grade)
      end_idx = all_grades.index(till_grade)

      if start_idx > end_idx:
         print("Invalid range: from_grade should be lower than till_grade.")
         return None

      selected_grades = all_grades[start_idx:end_idx + 1]
      cols = ['subjects'] + [g for g in selected_grades ]
      return self.df[cols]

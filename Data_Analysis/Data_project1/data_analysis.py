# Import Pandas library (like a digital spreadsheet)
import pandas as pd
from faker import Faker



# Load the CSV file
# Option 1: If you uploaded the CSV to Colab
data = pd.read_csv('student_activities.csv')

# Option 2: Create the CSV programmatically (if you don't want to upload)
csv_data = """StudentID,Grade,Activity,HoursPerWeek,Satisfaction,SleepingHours,StressLevel
1,9,Sports,5,4,6,3
2,10,Music,3,5,7,2
3,11,Gaming,8,3,5,4
4,9,Art,4,4,8,3
5,12,Sports,6,5,6,2
6,10,Gaming,10,4,5,5
7,11,Music,2,3,7,4
8,9,Sports,7,5,6,2
9,10,Art,5,4,8,3
10,12,Gaming,9,3,5,4
11,9,Music,3,4,7,3
12,11,Sports,4,5,6,2
13,10,Art,6,3,8,4
14,9,Gaming,7,4,5,3
15,12,Music,5,5,7,2
16,11,Sports,6,4,6,3
17,10,Gaming,8,3,5,4
18,9,Art,4,5,8,2
19,12,Sports,5,4,6,3
20,11,Music,3,3,7,4
21,9,Gaming,9,4,5,3
22,10,Sports,6,5,6,2
23,11,Art,5,4,8,3
24,12,Gaming,7,3,5,4
25,9,Music,4,5,7,2
26,10,Sports,8,4,6,3
27,11,Gaming,6,3,5,4
28,9,Art,3,4,8,3
29,12,Music,5,5,7,2
30,10,Sports,7,4,6,3
31,9,Gaming,8,3,5,4
32,11,Art,4,5,8,2
33,12,Sports,6,4,6,3
34,10,Music,3,3,7,4
35,9,Gaming,9,4,5,3
36,11,Sports,5,5,6,2
37,10,Art,6,4,8,3
38,12,Gaming,7,3,5,4
39,9,Music,4,5,7,2
40,11,Sports,8,4,6,3
41,10,Gaming,6,3,5,4
42,9,Art,5,4,8,3
43,12,Music,3,5,7,2
44,11,Sports,7,4,6,3
45,10,Gaming,8,3,5,4
46,9,Art,4,5,8,2
47,12,Sports,6,4,6,3
48,11,Music,5,3,7,4
49,10,Gaming,9,4,5,3
50,9,Sports,5,5,"""
with open('student_activities.csv', 'w') as file:
    file.write(csv_data)
data = pd.read_csv('student_activities.csv')

# Display the first 5 rows to check the data
print("First 5 rows of the data:")
print(data.head())

# Check for missing values
print("Checking for missing values:")
print(data.isnull().sum())

# Check for duplicates
print("\nChecking for duplicate rows:")
print(data.duplicated().sum())

# Ensure data types are correct
print("\nData types:")
print(data.dtypes)

# For this dataset, no cleaning is needed (no missing values or duplicates),
# but let's standardize the 'Activity' column to have consistent capitalization
data['Activity'] = data['Activity'].str.capitalize()

# Verify the changes
print("\nFirst 5 rows after cleaning:")
print(data.head())

# Count students per activity
activity_counts = data['Activity'].value_counts()
print("\nNumber of students per activity:")
print(activity_counts)

# Calculate average hours per week by activity
avg_hours = data.groupby('Activity')['HoursPerWeek'].mean().round(2)
print("\nAverage hours per week by activity:")
print(avg_hours)

# Count students per activity by grade
activity_by_grade = data.groupby(['Grade', 'Activity']).size().unstack(fill_value=0)
print("\nActivity counts by grade:")
print(activity_by_grade)

# Import Matplotlib for plotting
import matplotlib.pyplot as plt

# Bar chart for activity popularity
"""plt.figure(figsize=(8, 5))
activity_counts.plot(kind='bar', color='skyblue')
plt.title('Number of Students by Activity')
plt.xlabel('Activity')
plt.ylabel('Number of Students')
plt.xticks(rotation=0)
plt.show()"""

# Stacked bar chart for activities by grade
"""activity_by_grade.plot(kind='bar', stacked=True, figsize=(10, 6))
plt.title('Activities by Grade Level')
plt.xlabel('Grade')
plt.ylabel('Number of Students')
plt.legend(title='Activity')
plt.xticks(rotation=0)
plt.show()"""


"""avg_satisfaction = data.groupby('Activity')['Satisfaction'].mean().round(3)
print("\nAverage satisfaction by activity:")
print(avg_satisfaction)
# box plot for stress levels by activity
plt.figure(figsize=(8, 5))
data.boxplot(column='StressLevel', by='Activity', grid=False)
plt.title('Stress Levels by Activity')
plt.suptitle('')
plt.xlabel('Activity')
plt.ylabel('Stress Level')
plt.show()"""

# Calculate average stress level by activity
"""avg_stress = data.groupby('Activity')['StressLevel'].mean().round(3)
print("\nAverage stress level by activity:")
print(avg_stress)
# Scatter plot for hours per week vs. satisfaction
plt.figure(figsize=(8, 5))
plt.scatter(data['HoursPerWeek'], data['Satisfaction'], alpha=0.7)
plt.title('Hours Per Week vs. Satisfaction')
plt.xlabel('Hours Per Week')
plt.ylabel('Satisfaction')
plt.grid(True)
plt.show()"""
# pie chart for activity distribution
"""plt.figure(figsize=(6, 6))
activity_counts.plot(kind='pie', autopct='%1.1f%%', startangle=140, colors=plt.cm.Paired.colors)
plt.title('Activity Distribution')
plt.ylabel('')
plt.show()"""

#Relationship between sleeping hours and stress level
"""plt.figure(figsize=(8, 5))
plt.scatter(data['SleepingHours'], data['StressLevel'], alpha=0.7, color='orange')
plt.title('Sleeping Hours vs. Stress Level')
plt.xlabel('Sleeping Hours')
plt.ylabel('Stress Level')
plt.grid(True)
plt.show()"""

# Generate fake data using Fakerimport pandas as pd
import pandas as pd
from faker import Faker
import random

fake = Faker()

def generate_indian_number():
    # Mobile numbers in India usually start with 6,7,8,9
    first_digit = str(random.choice([6,7,8,9]))
    number = first_digit + ''.join([str(random.randint(0,9)) for _ in range(9)])
    return "+91" + number

data = []
for i in range(1,51):
    age = random.randint(12, 18)
    dob = fake.date_of_birth(minimum_age=age, maximum_age=age)
    
    data.append({
        "StudentID": i,
        "Age": age,
        "DOB": dob,
        "Email": fake.email(),
        "GuardianName": fake.name(),
        "GuardianContact": generate_indian_number()
    })

df = pd.DataFrame(data)
print(df.head())

# Save to CSV
df.to_csv("student_guardian_data.csv", index=False)


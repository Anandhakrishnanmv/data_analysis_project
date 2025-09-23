import pandas as pd
import matplotlib.pyplot as plt

# Load both datasets
activities_data = pd.read_csv('student_activities.csv')
guardian_data = pd.read_csv('student_guardian_data.csv')

# Merge datasets using StudentID as the common key
data = pd.merge(activities_data, guardian_data, on='StudentID', how='inner')

# Save merged dataset to a new CSV file
data.to_csv('merged_student_data.csv', index=False)
print("✅ Merged dataset saved as 'merged_student_data.csv'")

# Display information about the merged dataset
print("Merged dataset shape:", data.shape)
print("\nColumns in merged dataset:", list(data.columns))
print("\nFirst few rows of merged data:")
print(data.head())
print("\nMissing values in merged data:")
print(data.isnull().sum())



activities = ['Sports', 'Music', 'Gaming', 'Art']
filtered = data[data['Activity'].isin(activities)]
counts = filtered.groupby(['Grade', 'Activity']).size().unstack(fill_value=0)
print("\n",counts)

# Plot
counts.plot(kind='bar', figsize=(10, 6))
plt.title('Student Participation by Grade and Activity')
plt.xlabel('Grade')
plt.ylabel('Number of Students')
plt.legend(title='Activity')
plt.tight_layout()
plt.show()


# Group by activity and calculate average hours and satisfaction
summary = data.groupby('Activity')[['HoursPerWeek', 'Satisfaction']].mean().round(2)

# Plot
plt.figure(figsize=(8, 6))
plt.scatter(summary['HoursPerWeek'], summary['Satisfaction'], color='teal', s=100)

# Add labels
for activity, row in summary.iterrows():
    plt.text(row['HoursPerWeek'] + 0.1, row['Satisfaction'], activity, fontsize=9)

plt.title('Average Hours vs. Satisfaction by Activity')
plt.xlabel('Average Hours')
plt.ylabel('Average Satisfaction')
plt.grid(True)
plt.tight_layout()
plt.show()

# Additional analysis with merged data
print("\n" + "="*50)
print("ADDITIONAL ANALYSIS WITH MERGED DATA")
print("="*50)

# Analysis 1: Average satisfaction by age group
data['AgeGroup'] = pd.cut(data['Age'], bins=[10, 13, 15, 18], labels=['12-13', '14-15', '16-18'])
age_satisfaction = data.groupby('AgeGroup')['Satisfaction'].mean().round(2)
print("\nAverage Satisfaction by Age Group:")
print(age_satisfaction)

# Analysis 2: Activity participation by grade with guardian info
print("\nTop 5 most active students with guardian info:")
top_active = data.nlargest(5, 'HoursPerWeek')[['StudentID', 'Grade', 'Activity', 'HoursPerWeek', 'GuardianName']]
print(top_active)

# Analysis 3: Correlation between stress level and hours per week
correlation = data['StressLevel'].corr(data['HoursPerWeek'])
print(f"\nCorrelation between Stress Level and Hours Per Week: {correlation:.2f}")

# Analysis 4: Average hours by activity and grade
activity_grade_hours = data.groupby(['Activity', 'Grade'])['HoursPerWeek'].mean().round(2)
print("\nAverage Hours by Activity and Grade:")
print(activity_grade_hours)

# Analysis 5: Scatter plot of Stress Level vs Sleep Hours
plt.figure(figsize=(10, 6))
scatter = plt.scatter(data['SleepingHours'], data['StressLevel'],
                     c=data['Satisfaction'], cmap='viridis', s=50, alpha=0.7)

# Add colorbar
cbar = plt.colorbar(scatter)
cbar.set_label('Satisfaction Level')

# Add labels and title
plt.title('Relationship between Sleep Hours and Stress Level')
plt.xlabel('Sleeping Hours per Night')
plt.ylabel('Stress Level')
plt.grid(True, alpha=0.3)

# Add correlation coefficient
correlation_sleep_stress = data['SleepingHours'].corr(data['StressLevel'])
plt.text(0.05, 0.95, f'Correlation: {correlation_sleep_stress:.2f}',
         transform=plt.gca().transAxes, fontsize=12,
         verticalalignment='top', bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))

plt.tight_layout()
plt.show()

# Print summary statistics for this relationship
print(f"\nCorrelation between Sleep Hours and Stress Level: {correlation_sleep_stress:.2f}")
sleep_stress_summary = data.groupby('StressLevel')['SleepingHours'].agg(['mean', 'std', 'count']).round(2)
print("\nSleep Hours Statistics by Stress Level:")
print(sleep_stress_summary)

# Analysis 6: Students with High Stress Levels
print("\n" + "="*50)
print("STRESS LEVEL ANALYSIS")
print("="*50)

# Count students by stress level
stress_counts = data['StressLevel'].value_counts().sort_index()
print("\nNumber of Students by Stress Level:")
print(stress_counts)

# Define high stress levels (assuming 4-5 are high stress on a 1-5 scale)
high_stress_levels = [4, 5]
high_stress_students = data[data['StressLevel'].isin(high_stress_levels)]

print(f"\nStudents with HIGH stress (levels {high_stress_levels}):")
print(f"Total: {len(high_stress_students)} students ({len(high_stress_students)/len(data)*100:.1f}% of total)")

# Show details of high stress students
print("\nDetails of High Stress Students:")
high_stress_details = high_stress_students[['StudentID', 'Grade', 'Activity', 'StressLevel', 'SleepingHours', 'Satisfaction', 'GuardianName', 'GuardianContact', 'Email']]
print(high_stress_details.to_string())

# Create a focused report for high stress students with guardian details
print("\n" + "="*70)
print("HIGH STRESS STUDENTS REPORT - GUARDIAN CONTACT INFORMATION")
print("="*70)

for index, student in high_stress_students.iterrows():
    print(f"\nStudent ID: {student['StudentID']}")
    print(f"Grade: {student['Grade']}")
    print(f"Activity: {student['Activity']}")
    print(f"Stress Level: {student['StressLevel']}/5")
    print(f"Sleep Hours: {student['SleepingHours']} per night")
    print(f"Satisfaction: {student['Satisfaction']}/5")
    print(f"Activity Hours/Week: {student['HoursPerWeek']}")
    print("-" * 40)
    print(f"Guardian: {student['GuardianName']}")
    print(f"Contact: {student['GuardianContact']}")
    print(f"Email: {student['Email']}")
    print("=" * 70)

# Average characteristics of high stress students
print("\nAverage Characteristics of High Stress Students:")
high_stress_avg = high_stress_students[['SleepingHours', 'Satisfaction', 'HoursPerWeek']].mean().round(2)
print(high_stress_avg)

# Comparison with low stress students
low_stress_levels = [1, 2]
low_stress_students = data[data['StressLevel'].isin(low_stress_levels)]
print(f"\nStudents with LOW stress (levels {low_stress_levels}): {len(low_stress_students)} students")

low_stress_avg = low_stress_students[['SleepingHours', 'Satisfaction', 'HoursPerWeek']].mean().round(2)
print("Average Characteristics of Low Stress Students:")
print(low_stress_avg)

# Stress level distribution visualization
plt.figure(figsize=(10, 6))
stress_counts.plot(kind='bar', color='skyblue', edgecolor='black')
plt.title('Distribution of Stress Levels Among Students')
plt.xlabel('Stress Level')
plt.ylabel('Number of Students')
plt.xticks(rotation=0)
plt.grid(axis='y', alpha=0.3)

# Add percentage labels on bars
for i, count in enumerate(stress_counts):
    percentage = (count / len(data)) * 100
    plt.text(i, count + 0.5, f'{count}\n({percentage:.1f}%)', ha='center', va='bottom')

plt.tight_layout()
plt.show()

from faker import Faker

fake = Faker()

# print(fake.name())        # Random full name
# print(fake.address())     # Random address
# print(fake.email())       # Random email
# print(fake.date_of_birth())  # Random DOB
# print(fake.job())         # Random job title
# print(fake.company())     # Random company name
# print(fake.text(max_nb_chars=50))  # Random text snippet
# print(fake.random_int(min=18, max=65))  # Random integer between 18 and 65
# print(fake.random_element(elements=('A', 'B', 'C', 'D')))  # Random choice from a list

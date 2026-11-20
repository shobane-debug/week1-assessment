"""Solutions for the Week 1 Python & Data Engineering assessment."""
from __future__ import annotations


import csv
import json
import os
from pathlib import Path

from dotenv import load_dotenv
import numpy as np
import pandas as pd
import requests
import matplotlib.pyplot as plt


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
REPORTS = ROOT / "reports"
REPORTS.mkdir(exist_ok=True)


# Task 1: functions, OOP, custom exceptions, comprehensions and loops

def bonus(salary, rate=0.1, *extras, **options):
    """Return a bonus, including extras, optionally capped."""
    total = salary * rate + sum(extras)
    cap = options.get("cap")
    return min(total, cap) if cap is not None else total



class InvalidSalaryError(ValueError):
    """Raised when an employee salary is negative."""



class Employee:
    def __init__(self, name, salary):
        if salary < 0:
            raise InvalidSalaryError(f"Invalid salary: {salary}")
        self.name = name
        self.salary = salary



    def annual_salary(self):
        return self.salary * 12



    def get_details(self):
        return f"Employee: {self.name}, Salary: {self.salary}"



class Manager(Employee):
    def __init__(self, name, salary, team_size):
        super().__init__(name, salary)
        self.team_size = team_size



    def get_details(self):
        return f"Manager: {self.name}, Salary: {self.salary}, Team size: {self.team_size}"



def task1():
    employees = pd.read_csv(DATA / "employees.csv")
    names_over_50k = [row.name for row in employees.itertuples() if row.salary > 50000]
    raised = list(map(lambda salary: round(salary * 1.10, 2), employees.salary))
    chennai_names = list(filter(lambda city_name: city_name[1] == "Chennai", zip(employees.name, employees.city)))
    chennai_names = [name for name, _city in chennai_names]
    print("Above 50000:", names_over_50k)
    print("Chennai:", chennai_names)
    print("10% raise salaries:", raised)
    # Continue skips zero; break stops after first salary greater than 85,000.
    for salary in [0, 30000, 45000, 90000, 68000]:
        if salary == 0:
            continue
        print("Loop salary:", salary)
        if salary > 85000:
            break
    try:
        Employee("Test", -500)
    except InvalidSalaryError as error:
        print("Error:", error)
    finally:
        print("Transaction finished")
    print("Bonus example:", bonus(50000, 0.1, 1000, cap=6000))
    print(Employee("Arun", 30000).annual_salary())
    print(Manager("Priya", 75000, 5).get_details())


# Task 2: CSV/JSON, API, dotenv and error handling

def file_tasks():
    with (DATA / "employees.csv").open(newline="", encoding="utf-8") as csv_file:
        rows = list(csv.DictReader(csv_file))
    for row in rows:
        row["id"] = int(row["id"])
        row["salary"] = int(row["salary"])
    with (DATA / "employees.json").open("w", encoding="utf-8") as json_file:
        json.dump(rows, json_file, indent=2)
    high_earners = [row for row in rows if row["salary"] > 50000]
    with (DATA / "high_earners.csv").open("w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(high_earners)
    print(f"Rows read: {len(rows)} | High earners: {len(high_earners)}")

    load_dotenv(ROOT / ".env")
    api_key = os.getenv("API_KEY", "")  # Loaded securely; not required by JSONPlaceholder.
    if api_key:
        print("API_KEY loaded from .env")

    try:
        response = requests.get("https://jsonplaceholder.typicode.com/users", timeout=5)
        response.raise_for_status()
        users = response.json()
        for user in users[:3]:
            print(f'{user.get("id")} - {user.get("name")} - {user.get("email")}')
        # Demonstrate parsing a nested JSON field using .get().
        parsed = [
            {"id": user.get("id"), "name": user.get("name"),
             "city": user.get("address", {}).get("city"),
             "company": user.get("company", {}).get("name")}
            for user in users[:3]
        ]
        with (DATA / "users.json").open("w", encoding="utf-8") as output:
            json.dump(parsed, output, indent=2)
    except requests.exceptions.Timeout:
        print("API error: request timed out")
    except requests.exceptions.ConnectionError:
        print("API error: connection failed")
    except requests.exceptions.RequestException as error:
        print("API error:", error)

    try:
        missing_user = requests.get("https://jsonplaceholder.typicode.com/users/9999", timeout=5)
        print(f"/users/9999 -> {missing_user.status_code} Not found" if missing_user.status_code == 404 else f"/users/9999 -> {missing_user.status_code}")
    except requests.exceptions.Timeout:
        print("404 check: request timed out")
    except requests.exceptions.ConnectionError:
        print("404 check: connection failed")


# Task 3: NumPy, Pandas, data cleaning, aggregation, joins and charts

def task3():
    marks = np.array([[78, 82, 90], [88, 75, 92], [65, 70, 80], [95, 91, 89]])
    print("Marks shape:", marks.shape)
    print("Student averages:", marks.mean(axis=1))
    print("Subject averages:", marks.mean(axis=0))
    marks_with_grace = marks + 5  # broadcasting adds 5 to each value
    weights = np.array([0.3, 0.3, 0.4])
    print("Grace marks:\n", marks_with_grace)
    print("Weighted scores:", np.dot(marks, weights))

    df = pd.read_csv(DATA / "employees.csv")
    print("\nDataFrame info:")
    df.info()
    print("\nDescribe:\n", df.describe())
    print("loc sample:\n", df.loc[0:2, ["name", "salary"]])
    print("iloc sample:\n", df.iloc[0:3, 0:3])
    print("IT employees:\n", df[df["department"] == "IT"])

    messy = pd.read_csv(DATA / "employees_with_issues.csv")
    messy["salary"] = pd.to_numeric(messy["salary"], errors="coerce")
    messy = messy.drop_duplicates()
    median_salary = messy["salary"].median()
    messy["salary"] = messy["salary"].fillna(median_salary).astype(int)
    messy["id"] = messy["id"].astype(int)
    messy["salary"] = messy["salary"].astype(int)
    messy.to_csv(DATA / "employees_cleaned.csv", index=False)
    print(f"\nCleaning: duplicate rows removed; missing salaries filled with median {median_salary:.0f}.")

    summary = df.groupby("department").agg(
        headcount=("id", "count"), average_salary=("salary", "mean"), max_salary=("salary", "max")
    ).round(2)
    print("\nDepartment summary:\n", summary)
    departments = pd.read_csv(DATA / "departments.csv")
    inner = pd.merge(df, departments, on="department", how="inner")
    left = pd.merge(df, departments, on="department", how="left")
    outer = pd.merge(df, departments, on="department", how="outer", indicator=True)
    print("\nInner join rows:", len(inner), "Left join rows:", len(left))
    print("Outer join departments without employees:", outer.loc[outer["_merge"] == "right_only", "department"].unique().tolist())

    # Chart 1: headcount per department
    headcount = df.groupby("department")["id"].count()
    headcount.plot(kind="bar", title="Employee Headcount by Department", legend=True)
    plt.xlabel("Department"); plt.ylabel("Employees"); plt.legend(["Headcount"]); plt.tight_layout()
    plt.savefig(REPORTS / "department_headcount.png"); plt.close()
    # Chart 2: salary distribution
    df["salary"].plot(kind="hist", bins=5, title="Employee Salary Distribution", legend=True)
    plt.xlabel("Salary"); plt.ylabel("Frequency"); plt.legend(["Salary"]); plt.tight_layout()
    plt.savefig(REPORTS / "salary_histogram.png"); plt.close()
    # Chart 3: salary versus employee id
    df.plot(kind="scatter", x="id", y="salary", title="Salary by Employee ID", legend=True)
    plt.xlabel("Employee ID"); plt.ylabel("Salary"); plt.tight_layout()
    plt.savefig(REPORTS / "salary_scatter.png"); plt.close()
    # Chart 4: average salary by department
    summary["average_salary"].plot(kind="line", marker="o", title="Average Salary by Department", legend=True)
    plt.xlabel("Department"); plt.ylabel("Average Salary"); plt.legend(["Average salary"]); plt.tight_layout()
    plt.savefig(REPORTS / "average_salary_line.png"); plt.close()
    print("\nInsights:")
    print("1. IT has the highest headcount (3 employees).")
    print("2. Salaries span from 30,000 to 90,000 in this dataset.")
    print("3. Salary values are distributed across several levels; employee ID is only an identifier, not a causal factor.")
    print("4. Finance has the highest department average salary in this sample.")


if __name__ == "__main__":
    task1()
    file_tasks()
    task3()

---
# Invoice Management System

The Invoice Management System is a web application designed to streamline the process of generating and managing invoices for a educational institution. It allows users to create, view, and manage invoices for student payments, while also providing features to generate PDF invoices with embedded QR codes for easy tracking and verification.

![Invoice Management System](https://github.com/Levi-Chinecherem/invoice-management-system/blob/main/sample.png)

## Features

- **User Authentication and Authorization**: The system provides secure user registration and login functionalities. Users are categorized into roles, including admin and staff, with varying levels of access.
- **Payment Category Management**: Admins can define various payment categories, such as tuition, exam fees, library fines, etc., to classify different types of payments.
- **Student Information**: Students' information, including full name, department, level, school, and sex, can be entered and managed within the system.
- **Invoice Generation**: The system enables staff to generate invoices for specific payment categories, associating them with relevant students. Each invoice contains student and payment information.
- **QR Code Integration**: Invoices include QR codes that embed important payment details for easy scanning and verification. This ensures quick and accurate tracking of payments.
- **PDF Invoice Generation**: The system generates PDF invoices with embedded QR codes. These PDFs can be easily downloaded and shared, making them a convenient way to provide payment records.
- **Invoice Approval**: Admins can approve or reject generated invoices, updating the approval status accordingly.
- **Invoice Management**: Staff can view and manage invoices, including details such as payment category, amount, approval status, and creation date.

## How to Use

1. Clone the repository to your local machine:

```bash
git clone https://github.com/Levi-Chinecherem/invoice-management-system.git
```

2. Install project dependencies using a virtual environment:

```bash
cd invoice-management-system
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. Set up your database and configure settings in `settings.py`.
4. Run database migrations:

```bash
python manage.py migrate
```

5. Create a superuser account to access the admin panel:

```bash
python manage.py createsuperuser
```

6. Run the development server:

```bash
python manage.py runserver
```

7. Access the system via your web browser: [http://localhost:8000/](http://localhost:8000/)

## Benefits

- **Efficient Payment Management**: The system simplifies the process of generating invoices and tracking student payments, reducing manual effort and errors.
- **QR Code Verification**: QR codes make payment verification quick and accurate, enhancing transparency and reducing fraud.
- **PDF Invoices**: PDF invoices with embedded QR codes can be easily shared digitally, providing a reliable payment record.
- **User Roles and Permissions**: Role-based access control ensures that staff and admins have appropriate levels of access and authority.
- **Streamlined Workflow**: The system streamlines payment tracking and approval processes, improving overall efficiency and reducing administrative workload.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
---

# Problem Statement

## 1. Title
Online Pharmacy Ordering Platform

## 2. Domain
HealthTech / E-Pharmacy

## 3. Who is the user? (2-3 user types, with roles)
1. Customer/User - Can register, log in, browse medicines, upload prescriptions,
   add medicines to cart, place orders, and view order status.

2. Admin/Pharmacist - Can log in, manage medicines, view customer orders,
   verify uploaded prescriptions, and update order status.

## 4. What problem are we solving? (3-5 sentences, real-life example)
Customers often need to visit a physical pharmacy to check medicine availability
and purchase medicines. This can be inconvenient for elderly people, people who
are sick, or customers who cannot easily travel to a pharmacy. Customers also need
a convenient way to submit prescriptions and track their medicine orders.
The proposed system provides an online platform where customers can browse
available medicines, upload prescriptions when required, place orders, and track
their order status. Administrators can manage medicines, prescriptions, and
customer orders from a centralized system.

## 5. Proposed Solution (what the application will do, feature-wise)
The Online Pharmacy Ordering Platform will provide the following features:

### Customer Features
- User registration and login
- Browse available medicines
- Search medicines by name
- View medicine details and price
- Add medicines to cart
- Upload a prescription
- Place an order
- View previous orders
- Track order status

### Admin Features
- Admin login
- Add, edit, and remove medicines
- View registered customers
- View customer orders
- View and verify uploaded prescriptions
- Update order status
- Manage medicine availability

## 6. Core Entities / Database Tables (list all, minimum 5)
1. User
2. Medicine
3. Category
4. Prescription
5. Order
6. OrderItem
7. DeliveryTracking

## 7. User Roles & Permissions (minimum 2 distinct roles, e.g. Admin & User)

### Customer
- Register and log in
- Browse medicines
- Search medicines
- Add medicines to cart
- Upload prescriptions
- Place orders
- View orders
- Track order status

### Admin
- Log in to the admin account
- Add, edit, and delete medicines
- Manage medicine categories
- View customers
- View orders
- Verify prescriptions
- Update order and delivery status

## 8. Success Criteria
- A customer should be able to register and log in successfully.
- A customer should be able to browse available medicines.
- A customer should be able to add medicines to an order.
- A customer should be able to upload a prescription.
- A customer should be able to place an order successfully.
- An admin should be able to manage medicines and customer orders.
- A customer should be able to view the current status of their order.
- The application should store user, medicine, prescription, and order data
  correctly in the database.

## 9. Out of Scope (clearly list what you will NOT build, to avoid over-commitment)
The following features are outside the initial scope of this project:

- Real-money online payment processing
- Actual medicine delivery logistics
- Integration with real pharmacies or hospitals
- Automatic medical diagnosis
- Emergency medical services
- Video/audio consultation with doctors
- Prescription generation by doctors
- Real-time GPS delivery tracking

## 10. Chosen Track:
Python (FastAPI)
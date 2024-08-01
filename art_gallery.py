import streamlit as st
import pandas as pd
import mysql.connector

import streamlit as st
import base64
from PIL import Image, ImageFilter
import io


def get_image_base64(image_path):
    img = Image.open(image_path)
    img = img.convert("RGBA")

    # Create a new image with a semi-transparent black layer
    darkened = Image.new("RGBA", img.size, (0, 0, 0, 128))
    img = Image.alpha_composite(img, darkened)

    # Apply blur (you may need to install pillow-simd for better performance)
    img = img.filter(ImageFilter.GaussianBlur(radius=5))

    buffered = io.BytesIO()
    img.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode()


def set_bg_hack(main_bg):
    """
    A function to unpack an image from root folder and set as bg.
    """
    main_bg_ext = "png"

    st.markdown(
        f"""
         <style>
         .stApp {{
             background: url(data:image/{main_bg_ext};base64,{main_bg});
             background-size: cover;
         }}
         </style>
         """,
        unsafe_allow_html=True,
    )


def add_bg_from_local():
    image_files = [
        "assets/pic1.jpg",
        "assets/pic2.jpg",
        "assets/pic3.jpg",
        "assets/pic4.jpg",
    ]

    image_base64 = [get_image_base64(img) for img in image_files]

    st.markdown(
        f"""
    <style>
    .stApp {{
        background-image: url(data:assets/assets/pic1.jpg;base64,{image_base64[0]});
        background-size: cover;
        animation: slideshow 20s linear infinite;
    }}
    @keyframes slideshow {{
        0% {{ background-image: url(data:assets/pic1.jpg;base64,{image_base64[0]}); }}
        25% {{ background-image: url(data:assets/pic2.jpg;base64,{image_base64[1]}); }}
        50% {{ background-image: url(data:assets/pic3.jpg;base64,{image_base64[2]}); }}
        75% {{ background-image: url(data:assets/pic4.jpg;base64,{image_base64[3]}); }}
        100% {{ background-image: url(data:assets/pic1.jpg;base64,{image_base64[0]}); }}
    }}
    </style>
    """,
        unsafe_allow_html=True,
    )


# Call this function at the beginning of your app
add_bg_from_local()

# Rest of your Streamlit app code...


def load_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


# Call this function at the beginning of your app
load_css("style.css")


# Add this at the beginning of your script
def check_password():
    """Returns `True` if the user had the correct password."""

    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if st.session_state["password"] == st.secrets["password"]:
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # don't store password
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        # First run, show input for password.
        st.text_input(
            "Enter Password",
            type="password",
            on_change=password_entered,
            key="password",
        )
        return False
    elif not st.session_state["password_correct"]:
        # Password incorrect, show input + error.
        st.text_input(
            "Enter Password",
            type="password",
            on_change=password_entered,
            key="password",
        )
        st.error("😕 Password incorrect")
        return False
    else:
        # Password correct.
        return True


try:
    if st.session_state.current_page == "password":
        st.title("Welcome to Impression's Database")
except AttributeError:
    pass
if check_password():

    # Connect to your database
    cnx = mysql.connector.connect(
        user="root",
        password="Edemk22@2024",
        host="localhost",
        port=3307,
        database="artgallery",
    )

    # Create a cursor object
    cursor = cnx.cursor()

    # Define functions for each feature

    update_clicked = False
    add_clicked = False
    delete_clicked = False

    # Artwork Management
    def view_artworks():
        artworks_df = pd.read_sql("SELECT * FROM Artwork", cnx)
        st.table(artworks_df)

    def add_artwork():
        global add_clicked
        title = st.text_input("Title", key="add_artwork_title")
        date_created = st.date_input("Date Created", key="add_artwork_date")
        date_received = st.date_input("Date Received", key="add_date_received")
        genre = st.text_input("Genre", key="add_artwork_genre")
        estimated_value = st.number_input("Estimated Value", key="add_artwork_value")

        if st.button("Add Artwork", key="add_artwork_button") and not add_clicked:
            add_clicked = True
            cursor.execute(
                "INSERT INTO Artwork (Title, DateCreated, DateReceived, Genre, EstimatedValue) VALUES (%s, %s, %s, %s, %s)",
                (title, date_created, date_received, genre, estimated_value),
            )
            cnx.commit()
            add_clicked = False

    def update_artwork():
        global update_clicked
        artwork_id = st.number_input("Artwork ID", key="update_artwork_id")
        title = st.text_input("Title", key="update_artwork_title")
        date_created = st.date_input("Date Created", key="update_artwork_date")
        date_received = st.date_input("Date Received", key="update_date_received")
        genre = st.text_input("Genre", key="update_artwork_genre")
        estimated_value = st.number_input("Estimated Value", key="update_artwork_value")
        status = st.selectbox(
            "Status", ["Available", "Sold", "Loaned"], key="update_artwork_status"
        )
        if (
            st.button("Update Artwork", key="update_artwork_button")
            and not update_clicked
        ):
            update_clicked = True
            cursor.execute(
                "UPDATE Artwork SET Title = %s, DateCreated = %s,DateReceived =%s ,Genre = %s, EstimatedValue = %s, Status_ = %s WHERE ArtID = %s",
                (
                    title,
                    date_created,
                    date_received,
                    genre,
                    estimated_value,
                    status,
                    artwork_id,
                ),
            )
            cnx.commit()
            update_clicked = False

    def delete_artwork():
        global delete_clicked
        artwork_id = st.number_input("Artwork ID", key="delete_artwork_id")
        if (
            st.button("Delete Artwork", key="delete_artwork_button")
            and not delete_clicked
        ):
            delete_clicked = True
            cursor.execute("DELETE FROM Artwork WHERE ArtID = %s", (artwork_id,))
            cnx.commit()
            st.success("Artwork deleted successfully")
            delete_clicked = False

    # Artist Management
    def view_artists():
        artists_df = pd.read_sql("SELECT * FROM Artists", cnx)
        st.table(artists_df)

    def add_artist():
        global add_clicked
        artistID = st.number_input("Artist ID")
        # Check if ArtistID already exists
        cursor.execute("SELECT * FROM artists WHERE ArtistID = %s", (artistID,))
        existing_artist = cursor.fetchone()
        if existing_artist:
            st.error("Artist ID already exists")
        else:
            # Proceed with inserting the new record
            fname = st.text_input("First Name")
            lname = st.text_input("Last Name")
            address = st.text_input("Address")
            email = st.text_input("Email")
            if st.button("Add Artist") and not add_clicked:
                add_clicked = True
                cursor.execute(
                    "INSERT INTO artists (ArtistID, Fname, Lname, Address, Email) VALUES (%s, %s, %s, %s, %s)",
                    (artistID, fname, lname, address, email),
                )
                cnx.commit()
                # st.success("Artist added successfully")
                add_clicked = False

    def delete_artist():
        global delete_clicked
        artist_id = st.number_input("Artist ID", key="delete_artist_id")
        if st.button("Delete Artist") and not delete_clicked:
            delete_clicked = True
            cursor.execute("DELETE FROM Artists WHERE ArtistID = %s", (artist_id,))
            cnx.commit()
            # st.success("Artist deleted successfully")
            delete_clicked = False

    def list_artworks_by_artist():
        artist_id = st.number_input("Artist ID", key="get_artist_id")
        artworks_df = pd.read_sql(
            "SELECT * FROM Artists WHERE ArtistID = %s", cnx, params=(artist_id,)
        )
        st.table(artworks_df)

    # Customer and Transaction Handling
    def register_customer():
        fname = st.text_input("First Name")
        lname = st.text_input("Last Name")
        email = st.text_input("Email")
        phone_number = st.text_input("Phone Number")
        if st.button("Register Customer"):
            cursor.execute(
                "INSERT INTO Customers (FirstName, LastName, Email, PhoneNumber) VALUES (%s, %s, %s,%s)",
                (fname, lname, email, phone_number),
            )
            cnx.commit()

    def record_transaction():
        transaction_id = st.number_input("Transaction ID")
        customer_id = st.number_input("Customer ID")
        artwork_id = st.number_input("Artwork ID")
        transaction_date = st.date_input("Transaction Date")
        total_amount = st.number_input("Total Amount")
        payment_method = st.selectbox(
            "Payment Method", ["Cash", "Credit Card", "Debit Card", "Bank Transfer"]
        )

        cursor.execute("SELECT * FROM Customers WHERE CustomerID = %s", (customer_id,))
        customer = cursor.fetchone()

        if customer:
            cursor.execute("SELECT * FROM Artwork WHERE ArtworkID = %s", (artwork_id,))
            artwork = cursor.fetchone()

            if artwork:
                cursor.execute(
                    "INSERT INTO Transactions (CustomerID, ArtworkID, TransactionDate, TotalAmount, PaymentMethod) VALUES (%s, %s, %s, %s, %s)",
                    (
                        customer_id,
                        artwork_id,
                        transaction_date,
                        total_amount,
                        payment_method,
                    ),
                )
                cnx.commit()
                st.success("Transaction recorded successfully")
            else:
                st.error("Artwork not found. Please insert the artwork first.")
        else:
            st.error("Customer not found. Please insert the customer first.")

    def view_transaction_history():
        transactions_df = pd.read_sql("SELECT * FROM Transactions", cnx)
        st.table(transactions_df)

    # Loan Management
    def record_artwork_loan():
        artwork_id = st.number_input("Artwork ID")
        customer_id = st.number_input("Customer ID")
        loan_date = st.date_input("Loan Date")
        return_date = st.date_input("Return Date")

        cursor.execute("SELECT * FROM Artwork WHERE ArtID = %s", (artwork_id,))
        artwork = cursor.fetchone()

        if artwork:
            cursor.execute(
                "SELECT * FROM Customers WHERE CustomerID = %s", (customer_id,)
            )
            customer = cursor.fetchone()

            if customer:
                cursor.execute(
                    "INSERT INTO LoanedArt (ArtID, RecipientID, DateLoaned, DueDate) VALUES (%s, %s, %s, %s)",
                    (artwork_id, customer_id, loan_date, return_date),
                )
                cnx.commit()
                st.success("Loan recorded successfully")
            else:
                st.error("Customer not found. Please insert the customer first.")
        else:
            st.error("Artwork not found. Please insert the artwork first.")

    def view_loaned_artworks():
        loans_df = pd.read_sql("SELECT * FROM LoanedArt", cnx)
        st.table(loans_df)

    def mark_loan_returned():
        loan_id = st.number_input("Loan ID")
        if st.button("Mark Loan Returned"):
            cursor.execute(
                "UPDATE LoanedArt SET Returned = 1 WHERE ArtID = %s", (loan_id,)
            )
            cnx.commit()

    # Exhibition Management
    def create_exhibition():
        exhId = st.number_input("Exhibition ID", key="create_exhibition_id")
        title = st.text_input("Title")
        start_date = st.date_input("Start Date")
        end_date = st.date_input("End Date")
        wing = st.text_input("Gallery Wing")
        if st.button("Create Exhibition"):
            cursor.execute(
                "INSERT INTO Exhibition (ExhID, Theme, GalleryWing, StartDate, EndDate) VALUES (%s, %s, %s, %s, %s)",
                (exhId, title, wing, start_date, end_date),
            )
            cnx.commit()
            st.success("Exhibition created successfully!")

    def assign_artwork_to_exhibition():
        exhibition_id = st.number_input(
            "Exhibition ID", key="assign_artwork_to_exhibition"
        )
        artwork_id = st.number_input("Artwork ID")
        if st.button("Assign Artwork"):
            cursor.execute("SELECT * FROM Artwork WHERE ArtID = %s", (artwork_id,))
            artwork = cursor.fetchone()
            if artwork:
                cursor.execute(
                    "INSERT INTO ArtExhibitions (ExhibitionID, ArtID) VALUES (%s, %s)",
                    (exhibition_id, artwork_id),
                )
                cnx.commit()
                st.success("Artwork assigned to exhibition successfully")
            else:
                st.error("Artwork not found. Please insert the artwork first.")

    def view_artworks_in_exhibition():
        exhibition_id = st.number_input(
            "Exhibition ID", key="view_artworks_in_exhibition"
        )
        artworks_df = pd.read_sql(
            "SELECT * FROM Artwork WHERE ArtID IN (SELECT ArtID FROM ArtExhibitions WHERE ExhibitionID = %s)",
            cnx,
            params=(exhibition_id,),
        )
        st.table(artworks_df)

    def record_visitor_attendance():
        exhibition_id = st.number_input("Exhibition ID")
        visitor_id = st.number_input("Visitor ID")
        visited_date = st.date_input("Visited Date")
        if st.button("Record Attendance"):
            # Check if visitor exists
            cursor.execute("SELECT * FROM visitors WHERE VisitorId = %s", (visitor_id,))
            visitor = cursor.fetchone()
            if visitor:
                # Check if exhibition exists
                cursor.execute(
                    "SELECT * FROM Exhibition WHERE ExhID = %s", (exhibition_id,)
                )
                exhibition = cursor.fetchone()
                if exhibition:
                    cursor.execute(
                        "INSERT INTO VisitorExhibition (ExhibitionId, VisitorID, Visited) VALUES (%s, %s, %s)",
                        (exhibition_id, visitor_id, visited_date),
                    )
                    cnx.commit()
                    st.success("Visitor attendance recorded successfully")
                else:
                    st.error(
                        "Exhibition not found. Please insert the exhibition detail first."
                    )
            else:
                st.error("Visitor not found. Please insert the visitor detail first.")

    def add_employee():
        global add_clicked
        empID = st.number_input("Employee ID")
        fname = st.text_input("First Name")
        lname = st.text_input("Last Name")
        email = st.text_input("Email")
        department_id = st.number_input("Department ID")

        # Check if department exists
        cursor.execute(
            "SELECT * FROM Department WHERE DepartmentID = %s", (department_id,)
        )
        department = cursor.fetchone()

        if department:
            if st.button("Add Employee") and not add_clicked:
                add_clicked = True
                cursor.execute(
                    "INSERT INTO Employee (EmployeeID, FirstName, LastName, Email, DepartmentID) VALUES (%s, %s, %s, %s, %s)",
                    (empID, fname, lname, email, department_id),
                )
                cnx.commit()
                st.success("Employee added successfully")
                add_clicked = False
        else:
            st.error("Department not found")

    def view_employees():
        employees_df = pd.read_sql("SELECT * FROM Employee", cnx)
        st.table(employees_df)

    def update_employee():
        global update_clicked
        employee_id = st.number_input("Employee ID", key="update_employee_id")
        fname = st.text_input("First Name", key="update_fname")
        lname = st.text_input("Last Name", key="update_lname")
        email = st.text_input("Email", key="update_email")
        department_id = st.number_input("Department ID", key="update_department_id")
        if (
            st.button("Update Employee", key="update_employee_button")
            and not update_clicked
        ):
            update_clicked = True
            cursor.execute(
                "UPDATE Employee SET FirstName = %s, LastName = %s, Email = %s, DepartmentID = %s WHERE EmployeeID = %s",
                (fname, lname, email, department_id, employee_id),
            )
            cnx.commit()
            st.success("Employee updated successfully")
            update_clicked = False

    def delete_employee():
        global delete_clicked
        employee_id = st.number_input("Employee ID", key="delete_employee_id")
        if st.button("Delete Employee", key="delete_employee_button"):
            delete_clicked = True
            cursor.execute("DELETE FROM Employee WHERE EmployeeID = %s", (employee_id,))
            cnx.commit()
            st.success("Employee deleted successfully")
            delete_clicked = False

    def view_art_worth_more_than_average():
        query = """
            select aw.ArtID, aw.Title, aw.EstimatedValue, concat(ar.Fname," ", ar.Lname) as Artist
            from Artwork aw
            left outer join ArtArtists aa on aw.ArtID = aa.ArtID
            left outer join Artists ar on aa.ArtistID = ar.ArtistID
            left outer join LoanedArt la on aw.ArtID = la.ArtID
            group by Artist, aw.ArtID, aw.Title, aw.EstimatedValue, la.ArtID 
            having aw.EstimatedValue > (select avg(EstimatedValue) from Artwork)
            order by aw.EstimatedValue desc;
        """
        artworks_df = pd.read_sql(query, cnx)
        st.table(artworks_df)

    def view_art_older_than_1990():
        query = """
            select 
              a.Title,
              case when la.ArtID is null then 'Available' else 'Loaned' end as status,
              CONCAT(ar.Fname, ' ', ar.Lname) as ArtistName,
              year(a.DateCreated) as CreationYear
            from Artwork a
            inner join ArtArtists aa on a.ArtID = aa.ArtID
            inner join Artists ar on aa.ArtistID = ar.ArtistID
            left join LoanedArt la on a.ArtID = la.ArtID
            where year(a.DateCreated) < 1990
            order by CreationYear desc;
        """
        artworks_df = pd.read_sql(query, cnx)
        st.table(artworks_df)

    def view_available_artworks():
        query = """
            select a.ArtID,  a.Title, a.Status_, concat(ar.Fname, ' ', ar.Lname) as ArtistName
            from Artwork a
            inner join ArtArtists aa on a.ArtID = aa.ArtID
            inner join Artists ar on aa.ArtistID = ar.ArtistID
            where a.Status_ not in ('Sold', 'Loaned')
            order by a.ArtID;
        """
        artworks_df = pd.read_sql(query, cnx)
        st.table(artworks_df)

    def view_total_value_of_artworks_in_exhibition(exhibition_id):
        query = """
            select e.ExhID, e.Theme, SUM(a.EstimatedValue) as TotalValue
            from ArtExhibitions ae
            inner join Exhibition e on ae.ExhibitionID = e.ExhID
            inner join Artwork a on ae.ArtID = a.ArtID
            where e.ExhID = %s
            group by e.ExhID, e.Theme;
        """
        artworks_df = pd.read_sql(query, cnx, params=(exhibition_id,))
        st.table(artworks_df)

    def check_if_piece_is_scheduled_for_exhibition(artwork_title):
        query = """
            select e.Theme, e.GalleryWing, concat(e.StartDate, " to ", e.EndDate) as ExhibitionPeriod
            from ArtExhibitions ae
            inner join Exhibition e on ae.ExhibitionID = e.ExhID
            where ae.ArtID in (select ArtID from Artwork where Title like %s)
            order by e.StartDate;
        """
        artworks_df = pd.read_sql(query, cnx, params=("%" + artwork_title + "%",))
        st.table(artworks_df)

    def view_number_of_artworks_per_artist():
        query = """
            with ArtistArtwork as (
              select a.ArtistID, a.Fname, a.Lname, aw.Title
              from Artists a
              inner join ArtArtists aa on a.ArtistID = aa.ArtistID
              inner join Artwork aw on aa.ArtID = aw.ArtID
            )
            select concat(Fname, ' ', Lname) as Artist, COUNT(*) as ArtworkCount, group_concat(Title separator ', ') as ArtworkTitles
            from ArtistArtwork
            group by Fname, Lname
            order by ArtworkCount desc;
        """
        artworks_df = pd.read_sql(query, cnx)
        st.table(artworks_df)

    # Reporting and Analytics
    def generate_report():
        report_type = st.selectbox(
            "Report Type",
            [
                "Artwork Value",
                "Artwork Older Than 1990",
                "Available Artworks",
                "Total Value of Artworks in Exhibition",
                "Check if Piece is Scheduled for Exhibition",
                "Number of Artworks Per Artist",
            ],
        )
        if report_type == "Artwork Value":
            view_art_worth_more_than_average()
        elif report_type == "Artwork Older Than 1990":
            view_art_older_than_1990()
        elif report_type == "Available Artworks":
            view_available_artworks()
        elif report_type == "Total Value of Artworks in Exhibition":
            exhibition_id = st.number_input("Enter Exhibition ID")
            view_total_value_of_artworks_in_exhibition(exhibition_id)
        elif report_type == "Check if Piece is Scheduled for Exhibition":
            artwork_title = st.text_input("Enter Artwork Title")
            check_if_piece_is_scheduled_for_exhibition(artwork_title)
        elif report_type == "Number of Artworks Per Artist":
            view_number_of_artworks_per_artist()

    # Login section
    # with st.form("login"):
    # Create Streamlit pages
    # st.title("Art Gallery Database")

    # At the top of your script, after imports
    if "current_page" not in st.session_state:
        st.session_state.current_page = "Artwork Management"

    # Replace the sidebar buttons with a radio
    st.sidebar.title("Navigation")
    page = st.sidebar.radio(
        "Go to",
        [
            "Artwork Management",
            "Artist Management",
            "Customer and Transaction Handling",
            "Loan Management",
            "Exhibition Management",
            "Employee and Department Management",
            "Reporting and Analytics",
        ],
    )

    # Update the current page when radio selection changes
    if page != st.session_state.current_page:
        st.session_state.current_page = page

    # Render content based on the current page
    if st.session_state.current_page == "Artwork Management":
        st.title("Artwork Management")
        view_artworks()
        add_artwork()
        update_artwork()
        delete_artwork()
    elif st.session_state.current_page == "Artist Management":
        st.title("Artist Management")
        view_artists()
        add_artist()
        list_artworks_by_artist()
        delete_artist()
    elif st.session_state.current_page == "Customer and Transaction Handling":
        st.title("Customer and Transaction Handling")
        register_customer()
        record_transaction()
        view_transaction_history()
    elif st.session_state.current_page == "Loan Management":
        st.title("Loan Management")
        record_artwork_loan()
        view_loaned_artworks()
        mark_loan_returned()
    elif st.session_state.current_page == "Exhibition Management":
        st.title("Exhibition Management")
        create_exhibition()
        assign_artwork_to_exhibition()
        view_artworks_in_exhibition()
        record_visitor_attendance()
    elif st.session_state.current_page == "Employee and Department Management":
        st.title("Employee and Department Management")
        add_employee()
        view_employees()
        update_employee()
        delete_employee()
    elif st.session_state.current_page == "Reporting and Analytics":
        st.title("Reporting and Analytics")
        generate_report()

    query = st.text_area("Enter your SQL query", height=200)

    # Execute query button
    if st.button("Execute Query"):
        try:
            cursor.execute(query)
            results = cursor.fetchall()

            # Display the results in a table
            st.write("Query Results:")
            st.table(results)

        except Exception as e:
            # Display any errors that occur during execution
            st.error(f"Error executing query: {e}")

    # Close the cursor and connection
    cursor.close()
    cnx.close()
else:
    st.stop()

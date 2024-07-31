import streamlit as st
import pandas as pd
import mysql.connector

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


# Artwork Management
def view_artworks():
    artworks_df = pd.read_sql("SELECT * FROM Artwork", cnx)
    st.table(artworks_df)


def add_artwork():
    title = st.text_input("Title", key="add_artwork_title")
    date_created = st.date_input("Date Created", key="add_artwork_date")
    genre = st.text_input("Genre", key="add_artwork_genre")
    estimated_value = st.number_input("Estimated Value", key="add_artwork_value")
    status = st.selectbox(
        "Status", ["Available", "Sold", "Loaned"], key="add_artwork_status"
    )
    if st.button("Add Artwork", key="add_artwork_button"):
        cursor.execute(
            "INSERT INTO Artwork (Title, DateCreated, Genre, EstimatedValue, Status_) VALUES (%s, %s, %s, %s, %s)",
            (title, date_created, genre, estimated_value, status),
        )
        cnx.commit()


def update_artwork():
    artwork_id = st.number_input("Artwork ID", key="update_artwork_id")
    title = st.text_input("Title", key="update_artwork_title")
    date_created = st.date_input("Date Created", key="update_artwork_date")
    genre = st.text_input("Genre", key="update_artwork_genre")
    estimated_value = st.number_input("Estimated Value", key="update_artwork_value")
    status = st.selectbox(
        "Status", ["Available", "Sold", "Loaned"], key="update_artwork_status"
    )
    if st.button("Update Artwork", key="update_artwork_button"):
        cursor.execute(
            "UPDATE Artwork SET Title = %s, DateCreated = %s, Genre = %s, EstimatedValue = %s, Status_ = %s WHERE ArtID = %s",
            (title, date_created, genre, estimated_value, status, artwork_id),
        )
        cnx.commit()


# Artist Management
def view_artists():
    artists_df = pd.read_sql("SELECT * FROM Artists", cnx)
    st.table(artists_df)


def add_artist():
    fname = st.text_input("First Name")
    lname = st.text_input("Last Name")
    email = st.text_input("Email")
    if st.button("Add Artist"):
        cursor.execute(
            "INSERT INTO Artists (Fname, Lname, Email) VALUES (%s, %s, %s)",
            (fname, lname, email),
        )
        cnx.commit()


def list_artworks_by_artist():
    artist_id = st.number_input("Artist ID")
    artworks_df = pd.read_sql(
        "SELECT * FROM Artists WHERE ArtistID = %s", cnx, params=(artist_id,)
    )
    st.table(artworks_df)


# Customer and Transaction Handling
def register_customer():
    fname = st.text_input("First Name")
    lname = st.text_input("Last Name")
    email = st.text_input("Email")
    if st.button("Register Customer"):
        cursor.execute(
            "INSERT INTO Customers (Fname, Lname, Email) VALUES (%s, %s, %s)",
            (fname, lname, email),
        )
        cnx.commit()


def record_transaction():
    customer_id = st.number_input("Customer ID")
    artwork_id = st.number_input("Artwork ID")
    sale_date = st.date_input("Sale Date")
    if st.button("Record Transaction"):
        cursor.execute(
            "INSERT INTO Transactions (CustomerID, ArtworkID, SaleDate) VALUES (%s, %s, %s)",
            (customer_id, artwork_id, sale_date),
        )
        cnx.commit()


def view_transaction_history():
    transactions_df = pd.read_sql("SELECT * FROM Transactions", cnx)
    st.table(transactions_df)


# Loan Management
def record_artwork_loan():
    artwork_id = st.number_input("Artwork ID")
    loan_date = st.date_input("Loan Date")
    due_date = st.date_input("Due Date")
    if st.button("Record Loan"):
        cursor.execute(
            "INSERT INTO LoanedArt (ArtworkID, LoanDate, DueDate) VALUES (%s, %s, %s)",
            (artwork_id, loan_date, due_date),
        )
        cnx.commit()


def view_loaned_artworks():
    loans_df = pd.read_sql("SELECT * FROM LoanedArt", cnx)
    st.table(loans_df)


def mark_loan_returned():
    loan_id = st.number_input("Loan ID")
    if st.button("Mark Loan Returned"):
        cursor.execute(
            "UPDATE LoanedArt SET Returned = 1 WHERE LoanID = %s", (loan_id,)
        )
        cnx.commit()


# Exhibition Management
def create_exhibition():
    title = st.text_input("Title")
    start_date = st.date_input("Start Date")
    end_date = st.date_input("End Date")
    if st.button("Create Exhibition"):
        cursor.execute(
            "INSERT INTO Exhibitions (Title, StartDate, EndDate) VALUES (%s, %s, %s)",
            (title, start_date, end_date),
        )
        cnx.commit()
        st.success("Exhibition created successfully!")


def assign_artwork_to_exhibition():
    exhibition_id = st.number_input("Exhibition ID")
    artwork_id = st.number_input("Artwork ID")
    if st.button("Assign Artwork"):
        cursor.execute(
            "INSERT INTO ExhibitionArtworks (ExhibitionID, ArtworkID) VALUES (%s, %s)",
            (exhibition_id, artwork_id),
        )
        cnx.commit()


def view_artworks_in_exhibition():
    exhibition_id = st.number_input("Exhibition ID")
    artworks_df = pd.read_sql(
        "SELECT * FROM Artwork WHERE ArtID IN (SELECT ArtworkID FROM ExhibitionArtworks WHERE ExhibitionID = %s)",
        cnx,
        params=(exhibition_id,),
    )
    st.table(artworks_df)


def record_visitor_attendance():
    exhibition_id = st.number_input("Exhibition ID")
    visitor_count = st.number_input("Visitor Count")
    if st.button("Record Attendance"):
        cursor.execute(
            "INSERT INTO ExhibitionAttendance (ExhibitionID, VisitorCount) VALUES (%s, %s)",
            (exhibition_id, visitor_count),
        )
        cnx.commit()


# Employee and Department Management
def add_employee():
    fname = st.text_input("First Name")
    lname = st.text_input("Last Name")
    email = st.text_input("Email")
    department_id = st.number_input("Department ID")
    if st.button("Add Employee"):
        cursor.execute(
            "INSERT INTO Employee (Fname, Lname, Email, DepartmentID) VALUES (%s, %s, %s, %s)",
            (fname, lname, email, department_id),
        )
        cnx.commit()


def view_employees():
    employees_df = pd.read_sql("SELECT * FROM Employee", cnx)
    st.table(employees_df)


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
        where ae.ArtID = (select ArtID from Artwork where Title like %s)
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


# Create Streamlit pages
st.title("Art Gallery Database")

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
elif st.session_state.current_page == "Artist Management":
    st.title("Artist Management")
    view_artists()
    add_artist()
    list_artworks_by_artist()
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
elif st.session_state.current_page == "Reporting and Analytics":
    st.title("Reporting and Analytics")
    generate_report()

# Close the cursor and connection
cursor.close()
cnx.close()

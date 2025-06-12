# ELETRONIC CONSULT
#### Video Demo:  <URL HERE>
#### Description:
The project is a website for searching electronic components. Its main goal is to display data such as current and voltage for each searched component, either through direct queries or filter options.

To initially populate the database, a manual search was performed to fill in specifications for some commonly used components. These components were organized into categories such as capacitors, diodes, transistors, etc.

If a searched component is not found in the local database, the program attempts to fetch it using the Octopart API (Nexar API). The implementation of this API query relied heavily on the help of ChatGPT, which was also essential for working with the database via SQLAlchemy. Bootstrap was used for styling the pages, including the navigation bar, input fields for filters, and the search results layout.

Since the Nexar API has usage limits and requires a paid plan, the site may fail to retrieve data for components not in the local database. To handle this, any API error message is displayed on the search results page for transparency.

The project includes four .html files:

index.html – where filtered searches are performed,

layout.html – defines the general layout, including the navigation bar and links to category-based searches,

category.html – displays components belonging to a selected category,

search.html – shows results from filtered searches or direct queries through the navbar.

The core of the project is in app.py, which begins with the database configuration. Two additional files are used for working with the database:

models.py, which defines the database schema using SQLAlchemy, and

a script to insert data from a .csv file into the database, which depends on models.py for column definitions and keys.

Still in app.py, the API credentials (client ID and secret) are set, followed by the function that queries Nexar’s database to retrieve relevant component information.

The / (index) route simply renders index.html, the query with filters is passed to /search in the html file. The /search route handles the main search logic: it first tries to find the component in the local database using request.form.get() to extract filters, then applies these filters to the query. If no matching component is found, the code calls the Nexar API. If the component is found there, its data is shown in search.html and also saved to the local database for future use—this avoids hitting the API again, which helps stay within the query limits.

The /category/<cat> route follows the DRY principle to minimize duplicated route code. Depending on the category selected from the navbar (e.g., Capacitor, Diode), it displays all components from that category stored in the local database.

The /debug route is used for debugging purposes, simply listing all entries in the database to verify that everything is working correctly.

At the end of the program, there's a block that creates the database if it doesn't already exist.
The prints statementes that exist throughout the code are only for debugging purposes, they were placed as comments so that they can be reused if necessary.



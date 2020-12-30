My project is an application for finding and tracking hikes/trails.

I built the application using Python/Flask and a SQLite Database to store the user/hike data.
The application also relies on two external APIs (hiking project and mapquest).

![Log in page](https://i.ibb.co/pPXBQ8p/one.png)


A user can create an account by signing up, upon creation of a valid account (which is added to 'users' table in the database) the user is then redirected to the 'log in' page.
Once the user logs in successfully they are taken to the 'my hikes' page which displays all of their saved hikes.
In the case that they have no hikes saved they are automatically redirected to the 'add' page.

Add page:
On the 'add' page a user can enter a name, description and difficulty rating of a hike they have done into a form.
This data is then added to the 'hikes' table in the SQLite Database, along with the active users id.

![add page](https://i.ibb.co/txM2gkN/two.png)


My hikes page:
The 'hikes' table in the database is queried for the active users hikes and that data is then rendered on the page.
A user can also delete a hike, which then removes from it the 'hikes' table

![my hikes page](https://i.ibb.co/HPTpv7N/five.png)

Find page:
The user can enter a city name and the data of hikes within a 50 mile radius will be rendered below
When user submits the form firstly the city name is passed into a Geocoding API (mapquest) which returns the latitude and longitude of that city.
The returned lat/lon values are then used to make a call to the Hiking Project API which returns trail info on hikes within a 50 mile radius of those coordinates.
The data is then used to populate/render the results below. An if statement is then used to convert the difficulty to the rating used for my application.
A user can also click 'add' to add one of the results to their 'my hikes', thus adding to to the 'hikes' table in the database.

![find page](https://i.ibb.co/wNkTV38/four.png)


Logout page:
This logs a user out and closes their session


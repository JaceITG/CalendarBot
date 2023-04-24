# CalendarBot

Discord Event Planner and Calendar Bot

## Demonstration

### Creating a new event

Using a text channel in a Discord server where CalendarBot is enabled, we can register an account and create our first event using the slash command `/create` with arguments for the event's name, start time, and end time.

![Create command](https://i.imgur.com/xjNeAJQ.png)

This will convey a Create request to the scheduler (`await scheduler.request('create', [name, sdt, edt, ctx.author])`) which initializes a new user account and event document in the calendar database.

![Database entry](https://i.imgur.com/WLFZxq0.png)

Once the event is successfully created in the database, CalendarBot responds with an overview of the new document.

![Event created embed](https://i.imgur.com/Uo0foRs.png)

Start and end time arguments for the event are parsed from natural language, allowing for the interpretation of a variety of date-time formats and relative times such as "now"

![Different time formats](https://i.imgur.com/GDLVVEf.png)

### Reading events from the database

Existing event objects can be queried using the `/get` slash command. Events can be referenced by keyword arguments `name`, `id`, or `creator`. Additionally, the `query` argument can be used to filter the database using one or more expressions with the available event properties.

Let's conduct a simple search for the event we just created in the previous stage. Using its name, we can pull up the information for the event as such:

![/get name: GH201 Final](https://i.imgur.com/uYcR1xA.png)

Using queries with the `/get` command allows for more advanced filtering and aggregation of events. For example, querying all events with "final in name" will return a list of all final exams we have stored in the database.

![Final exams](https://i.imgur.com/Up42xR8.png)

Another typical use case for queries is to find events before or after a given date-time. Shown below is a query for all of Jace's events which start before May 3rd, 2023:

![Events before May 3rd](https://i.imgur.com/YNJH3kJ.png)

### Deleting events

Users may only delete their own events from the database, so delete requests sent to the scheduler are accompanied by a filter with the message author's ID
`await scheduler.request('delete', doc={'_id': id, 'author_id': int(ctx.author.id)})`

If we want to delete the event listing for "Homework", we can index it by the ID displayed in the last query shown above to ensure the correct event is removed.

![Delete Homework](https://i.imgur.com/JjfuOhI.png)

### Common errors

Errors in user input may commonly arise when attempting to interface with the database. For this reason, exceptions are caught and the [error embed utility](utils.py) returns a readable notice of the error to the user.

Some normal input errors include:

- Invalid time formats ![Invalid time format](https://i.imgur.com/9x90eNO.png)

- Malformed or invalid query expressions ![Invalid query property](https://i.imgur.com/f92MuiK.png) ![Malformed expression](https://i.imgur.com/byS5Wza.png)

- Failure to find/delete an event ![Missing event](https://i.imgur.com/QBatu93.png)

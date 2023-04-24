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

### Reading events from the database

Existing event objects can be queried using the `/get` slash command. Events can be referenced by keyword arguments `name`, `id`, or `creator`. Additionally, the `query` argument can be used to filter the database using one or more expressions with the available event properties.

Let's conduct a simple search for the event we just created in the previous stage. Using its name, we can pull up the information for the event as such:

![/get name: GH201 Final](https://i.imgur.com/uYcR1xA.png)

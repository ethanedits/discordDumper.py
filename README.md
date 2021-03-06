# discordDumper.py
This is a discord bot that will launch csgo, dump offsets (Memory Addresses), then close the process again. This can be done remotely from the discord app.

To add this bot to your discord server just replace the blank space on the ```client.run(' ')``` line to be your discord app token.

If you want to add another offset, duplicate the ```dwLocalPlayer(ctx)``` function as shown below:

![Image of Bot](https://media.discordapp.net/attachments/733974815735808041/735310388618592316/unknown.png)

Now replace any instances of dwLocalPlayer with the offset of your choice. Also replace the modulename, pattern, extra and offset with the proper one for that offset. To find the right pattern go to the hazedumper's ```config.json``` here: https://github.com/frk1/hazedumper/blob/master/config.json

Make sure the formatting for your pattern is correct. Each byte needs to be separated with a ```\x``` and all question marks (?) need to be replaced with a ```.```

Here is an example using dwEntityList ```\xBB....\x83\xFF\x01\x0F\x8C....\x3B\xF8```

Now find the extra and offset, add them after the pattern (extra comes first then offset) and separate them with a comma.

We also need to find the proper modulename, or the dll that we need to access. Most offsets will use the ```client.dll``` while others will use ```engine.dll``` This will come before the pattern.

Once completed it should look like this: ```'client.dll', rb'\xBB....\x83\xFF\x01\x0F\x8C....\x3B\xF8', 0, 1```

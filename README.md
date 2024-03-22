# Setup of Integration

You require 2 things:
- **token**
- **channel_id**

## 1.Create Discord Bot to get the token
![image](https://github.com/teki9ll/Discord-Integration-using-Webhooks/assets/95670904/7bf19491-669a-4eb9-84d3-dc74639850ee)
![image](https://github.com/teki9ll/Discord-Integration-using-Webhooks/assets/95670904/a5fa36dc-2fba-4500-80d1-623cf74172f7)

###Copy the generated link to invite the bot in your server. 

## 2.Getting Channel Id
In your discord, go to Settings, Advanced and turn on Developer Mode.
![image](https://github.com/teki9ll/Discord-Integration-using-Webhooks/assets/95670904/e797deea-a05f-41ac-8b40-1cb13caba128)

### Then Right Click on Channel name to get its id
![image](https://github.com/teki9ll/Discord-Integration-using-Webhooks/assets/95670904/2f294e46-ba02-4a7b-97b7-027437063618)


# Difference Between aiohttp and requests

When working with web requests in Python, two popular libraries often come into consideration: `aiohttp` and `requests`. Here's a quick summary of their differences:

## aiohttp

- **Asynchronous:** `aiohttp` is designed for asynchronous operations, making it ideal for I/O-bound tasks.
- **Concurrent Operations:** It allows for concurrent HTTP requests without blocking the event loop.
- **Performance:** Offers better performance when dealing with many requests in parallel.
- **Requires Event Loop:** `aiohttp` requires an event loop to run properly, using `async` and `await` syntax.

## requests

- **Synchronous:** `requests` is a synchronous library, blocking the execution until a response is received.
- **No Event Loop:** It does not require an event loop and follows a traditional synchronous programming model.
- **Simplicity:** Easier to use for simple, sequential requests.
- **Not Ideal for Asynchronous Tasks:** Can cause issues with I/O-bound operations and performance in asynchronous applications.

## Problem with requests and Immediate Message Retrieval

In scenarios where you send a message and immediately try to retrieve it using `requests`, you might face timing issues. This happens because the message might not have been fully processed and available on Discord's end.

A common error you might encounter is "message does not exist" because the message hasn't propagated through the system yet. 

### Using `concurrent.futures.ThreadPoolExecutor`

To mitigate some of these issues, you can use `concurrent.futures.ThreadPoolExecutor` to run tasks concurrently in a separate thread.

## Caution
However, even with ThreadPoolExecutor, there might still be timing issues due to the inherent nature of synchronous requests. To fully avoid these problems, especially in asynchronous applications, using aiohttp or another asynchronous library would be recommended.
 

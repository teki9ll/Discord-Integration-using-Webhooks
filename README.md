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

To mitigate some of these issues, you can use `concurrent.futures.ThreadPoolExecutor` to run tasks concurrently in a separate thread. Here's an example of how to use it with `requests`:

## Caution
However, even with ThreadPoolExecutor, there might still be timing issues due to the inherent nature of synchronous requests. To fully avoid these problems, especially in asynchronous applications, using aiohttp or another asynchronous library would be recommended.
 

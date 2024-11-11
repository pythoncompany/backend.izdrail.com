# Backend

This is the backend of my personal website.
This documentation assumes that you are familiar with: Linux, Docker, and Python.
If you don't know how to use these technologies, you can use the Live API which is available at [backend.izdrail.com](https://backend.izdrail.com/docs).

## Getting Started

If you are interested in using this API, you can follow these steps to get started:

1. Clone the repository.
```asciidoc
git clone https://github.com/pythoncompany/backend.izdrail.com.git
```
2. Navigate to the project directory.
3. Run the following command to start the API server.
```asciidoc
make build
```
4.
For more details, refer to the [Terms of Service](https://izdrail.com/terms/) provided by [Python Company](https://izdrail.com).

## API Endpoints

- **POST /feed/reader:** Fetch news feed.
- **POST /feed/finder:** Find relevant feeds.
- **POST /run/scrapper:** Run a web scraper.
- **POST /jobs:** Searches fo jobs.
- **GET /google/trending:** Get trending Google searches.
- **POST /google/news/search:** Search Google News.
- **POST /google/news/topic:** Get news on a specific topic.
- **POST /seo/analyze:** Analyze SEO for a given link.
- **POST /seo/lighthouse:** Run Lighthouse SEO analysis.
- **POST /nlp/article:** Perform NLP analysis on an article.
- **POST /videos/youtube:** Search for videos on YouTube.
- **GET /:** Root endpoint.

For detailed information on request and response formats, refer to [docs](https://backend.izdrail.com/docs).
The url provides and interactive documentation for the API.
## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
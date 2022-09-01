<!-- Improved compatibility of back to top link: See: https://github.com/othneildrew/Best-README-Template/pull/73 -->
<a name="readme-top"></a>
<!--
*** Thanks for checking out the Best-README-Template. If you have a suggestion
*** that would make this better, please fork the repo and create a pull request
*** or simply open an issue with the tag "enhancement".
*** Don't forget to give the project a star!
*** Thanks again! Now go create something AMAZING! :D
-->



<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->
[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]



<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/ben-m-90/stock_sim">
    <img src="images/logo.png" alt="Logo">
  </a>

<!-- <h3 align="center">project_title</h3> -->

  <p align="center">
    Practice trading strategies in a risk free environment.
    <br />
    <a href="https://github.com/ben-m-90/stock_sim"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/ben-m-90/stock_sim/issues">Report Bug</a>
    ·
    <a href="https://github.com/ben-m-90/stock_sim/issues">Request Feature</a>
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

[![Product Name Screen Shot][product-screenshot]](https://example.com)

Django web app which scrapes live stock market data and allows users to buy & sell stocks to test their trading strategies in a risk-free environment. Data is stored to SQL database with updates made just in time when user views page requiring data and only if data hasn’t been updated recently to reduce database demand.
* User account system. Users can create stock portfolios with whatever initial balance they want. Test how you would do with $1,000,000 or challenge yourself with $50.
* Data is scraped from Yahoo Finance. Prices are updated on demand (only when a user is viewing an element that requires displaying the price) and other data is updated on demand every hour.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



### Built With

* [![Django][Djangoproject.com]][Django-url]
* [![Bootstrap][Bootstrap.com]][Bootstrap-url]
* [![JQuery][JQuery.com]][JQuery-url]
* [![PostgreSQL][PostgreSQL.org]][PostgreSQL-url]

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- GETTING STARTED -->
## Getting Started

### Prerequisites

Before beginning setup, it is recommended to [https://docs.python.org/3/tutorial/venv.html#creating-virtual-environments](create and activate a Python virtual environment).

### Installation

1. Get a free API Key at [https://example.com](https://example.com)
2. Clone the repo
    ```sh
    git clone https://github.com/ben-m-90/stock_sim.git
    ```
3. Navigate your terminal to the local storage location created in Step 2.
4. Install packages from requirements.txt
    ```sh
    pip install -r requirements.txt
    ```
4. Download and install an SQL server. PostgreSQL was used to develop this project so it is recommended.
5. Rename the file 'sample.env' to '.env'
6. Edit '.env' using a text editor.
* ENGINE_DB_PATH, DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, and DB_PORT are values set during SQL database creation.
* See [https://docs.djangoproject.com/en/4.1/ref/databases/](Django database documentation) for more information.
* A Django Secret Key can be generated online. Simply copy and paste for DJANGO_SECRET_KEY.
    '''
    # .env

    ENGINE_DB_PATH = "postgresql+psycopg2://postgres:PASSWORD@localhost:5432/DATABASE_NAME"
    DJANGO_SECRET_KEY = 

    DB_ENGINE = "django.db.backends.postgresql_psycopg2"
    DB_NAME = ""
    DB_USER = ""
    DB_PASSWORD = ""
    DB_HOST = "127.0.0.1"
    DB_PORT = "5432"
    '''
7. Run the Django localserver in your terminal. Note that the shortcut py may not work on all systems and is dependent on how your local Python installation is configured.
    '''sh
    py manage.py runserver
    '''
8. Navigate to localhost:8000 in your web browser.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- USAGE EXAMPLES -->
## Usage

1. Create a new user account and log-in. E-mail verification will appear in the terminal the local server is running on.
2. Configure user settings by clicking the profile icon at the top right of the home page and selecting 'Settings'.
3. Create a new stock portfolio within user settings.
4. Navigate to a stock page by going to url localhost:8000/stock_details/"TICKER"
5. View information of the chosen stock and buy/sell the stock being viewed.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- ROADMAP -->
## Roadmap

- [ ] Implement initialization function to create Stock objects enmasse on startup.
- [ ] Implement database bulk update functionality to update all stocks on a schedule rather solely on-demand.
- [ ] Add feature to make call type trades (buy/sell at specific price)
- [ ] Add feature(s) for highlighting trending stocks

See the [open issues](https://github.com/ben-m-90/stock_sim/issues) for a full list of proposed features (and known issues).

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTACT -->
## Contact

Project Link: [https://github.com/ben-m-90/stock_sim](https://github.com/ben-m-90/stock_sim)

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

* [https://djangoproject.com/](Django)
* [https://github.com/ranaroussi/yfinance](yfinance)

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/ben-m-90/stock_sim.svg?style=for-the-badge
[contributors-url]: https://github.com/ben-m-90/stock_sim/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/ben-m-90/stock_sim.svg?style=for-the-badge
[forks-url]: https://github.com/ben-m-90/stock_sim/network/members
[stars-shield]: https://img.shields.io/github/stars/ben-m-90/stock_sim.svg?style=for-the-badge
[stars-url]: https://github.com/ben-m-90/stock_sim/stargazers
[issues-shield]: https://img.shields.io/github/issues/ben-m-90/stock_sim.svg?style=for-the-badge
[issues-url]: https://github.com/ben-m-90/stock_sim/issues
[license-shield]: https://img.shields.io/github/license/ben-m-90/stock_sim.svg?style=for-the-badge
[license-url]: https://github.com/ben-m-90/stock_sim/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/ben-a-miller
[product-screenshot]: images/screenshot.png
[Next.js]: https://img.shields.io/badge/next.js-000000?style=for-the-badge&logo=nextdotjs&logoColor=white
[Next-url]: https://nextjs.org/
[React.js]: https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB
[React-url]: https://reactjs.org/
[Vue.js]: https://img.shields.io/badge/Vue.js-35495E?style=for-the-badge&logo=vuedotjs&logoColor=4FC08D
[Vue-url]: https://vuejs.org/
[Angular.io]: https://img.shields.io/badge/Angular-DD0031?style=for-the-badge&logo=angular&logoColor=white
[Angular-url]: https://angular.io/
[Svelte.dev]: https://img.shields.io/badge/Svelte-4A4A55?style=for-the-badge&logo=svelte&logoColor=FF3E00
[Svelte-url]: https://svelte.dev/
[Laravel.com]: https://img.shields.io/badge/Laravel-FF2D20?style=for-the-badge&logo=laravel&logoColor=white
[Laravel-url]: https://laravel.com
[Bootstrap.com]: https://img.shields.io/badge/Bootstrap-563D7C?style=for-the-badge&logo=bootstrap&logoColor=white
[Bootstrap-url]: https://getbootstrap.com
[JQuery.com]: https://img.shields.io/badge/jQuery-0769AD?style=for-the-badge&logo=jquery&logoColor=white
[JQuery-url]: https://jquery.com 
[Djangoproject.com]: https://img.shields.io/badge/Django-20aa76?style-for-the-badge&logo=django&logoColor=white
[Django-url]: https://djangoproject.com
[PostgreSQL.org]: https://img.shields.io/badge/PostgreSQL-4169E1?style-for-the-badge&logo=postgresql&logoColor=white
[PostgreSQL-url]: https://postgresql.org

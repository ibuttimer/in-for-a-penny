- [InForAPenny Planning](#inforapenny-planning)
  - [Requirements](#requirements)
    - [Must haves](#must-haves)
    - [Optional extra](#optional-extra)
  - [Application ideas](#application-ideas)
    - [Idea 1](#idea-1)
      - [Outline](#outline)
      - [Features](#features)
      - [Resources](#resources)
    - [Idea 2](#idea-2)
      - [Outline](#outline-1)
  - [Frameworks](#frameworks)
    - [Full Stack](#full-stack)
    - [Frontend](#frontend)
      - [Comparison](#comparison)

# InForAPenny Planning
Project planning outline.

## Requirements
### Must haves
- Finance-related application
- Utilise at least one third party API

### Optional extra
- CSS framework other than Bootstrap

## Application ideas
### Idea 1
#### Outline
- Users have a portfolio to which that can add:
  - currency amounts
  - number of various stocks
- Users can add/subtract from individual portfolio items 
- User can choose a base currency in which their net worth will be estimated  
- Use FX API to convert currency amounts to base currency for net worth estimation
- Use stock API to convert stock values to base currency for net worth estimation
- App can estimate future net worth, e.g. next month
  - Something simple, calculate mean increase/decrease of currencies and stocks over previous estimate timeframe, e.g. last month

#### Features
- Use charting library to graph value of individual portfolio items and overall net worth

#### Resources
- [Chart.js](https://www.chartjs.org/docs/latest/)

### Idea 2
#### Outline
![TODO](https://img.shields.io/badge/TODO-yellow)

## Frameworks
### Full Stack
- [Django](https://www.djangoproject.com/)

### Frontend
Some options are
- [Bootstrap](https://getbootstrap.com/)
- [Materialize](https://materializecss.com/)
- [MDBootstrap](https://mdbootstrap.com/)

#### Comparison
Quick comparison summary based on 
- [Bootstrap vs Materialize](https://stackshare.io/stackups/bootstrap-vs-materialize#:~:text=The%20main%20difference%20is%20that,your%20code%20to%20Material%20Design.)
- [Bootstrap vs Materialize: What makes them similar?](https://htmlburger.com/blog/bootstrap-vs-materialize-review/)
- [Bootstrap vs Material: Which One is Better?](https://jelvix.com/blog/bootstrap-vs-material)

|              |             Bootstrap             | Materialize  |            MDBootstrap            |
|--------------|:---------------------------------:|:------------:|:---------------------------------:|
| Popularity   |                 1                 |      2       |                 ?                 |
| Responsive   |              &check;              |   &check;    |              &check;              |
| Appearance   |                 2                 |      1       |                 1                 |
| Components   |              &check;              |   &check;    |       &check;                     |
| Focus        | mobile and desktop (mobile-first) | mobile-first | mobile and desktop (mobile-first) |
| Dev speed    |                 1                 |      2       |                1?                 |
| Extra points |              &cross;              |   &check;    |              &check;              |

## Financial API
There are any number: 
- Exchange rates
  - [fixer](https://fixer.io/) (mentioned in Intro Webinar)
- Stocks
  - [YahooFinance Stocks](https://rapidapi.com/integraatio/api/yahoofinance-stocks1/) (have used in the past for historical stock prices)

## Database
- [ElephantSQL](https://www.elephantsql.com/)

## Deployment
Options are
- [Heroku](https://www.heroku.com/)
- [render](https://render.com/)




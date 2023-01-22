# Dara Planner

## Team Name: InForAPenny

[Dara Planner](https://dara-planner.herokuapp.com/)

## Contents(#contents)

* [User Experience (UX)](#user-experience)
    * [User Stories](#user-stories)
* [Technology](#technology)
* [Design](#design)
    * [Color Scheme](#color-scheme)
    * [Typography](#typography)
    * [Imagery](#imagery)
    * [Wireframes](#wireframes)
* [Deployment & Usage](#deployment)
* [Testing](#testing)
* [Credits](#credits)
    * [Code](#code)
    * [Content](#content)
    * [Media](#media)
    * [Acknowledgements](#acknowledgements)

## User Experience
<< what paradigms of user experience did you consider, and cater to? >>

### User stories
<< user stories here - don't be stingy on this 😅 you can even put down your expectations as a developer in this forum >>

## Technology:

<< Detail your techstack here, and why you chose it. >>

<< list your languages & tools below: >>

*  << languages >>
    * << list the langauge & reason for using it >>

* << tools >>
    * << list the tool & reason for using it >>

## Initial MVP idea:

Detail plans and scope of project here....

<< consider talking about how you planned as a team here and what tools were implemented >>

### Actual idea & content:

<< how does you final product/project match up to your initial mvp plans >>

<< detail idea / features / functionality here >>

## Design

### Color Scheme:
<< detail your color palette here >>

### Typography:
<< what font pairings did your team consider and pick? And why? >>

### Imagery:
<< Detail imagery used to compliment your build & theme >>

<< ensure source attribution is maintained, and that you have used copyright free material >>

### Wireframes:

<details>
<summary>- Mobile Wireframes:</summary>

<< put all your mobile wireframes here... >>

<< consider adding some notes to detail the planned components or functionality >>

</details>

<details>
<summary>- Desktop Wireframes:</summary>

<< put all your mobile wireframes here... >>

<< consider adding some notes to detail the planned components or functionality >>

</details>

## Deployment
<< detail deployment methods used here, and any extraneous circumstances to run the project locally >>
### Development and Local Deployment
#### Environment
The development environment requires:

| Artifact                                 | Download and installation instructions               |
|------------------------------------------|------------------------------------------------------|
| [git](https://git-scm.com/)              | https://git-scm.com/downloads                        |
| [Python](https://www.python.org/)        | https://www.python.org/downloads/                    |
| [Django](https://www.djangoproject.com/) | https://www.djangoproject.com/download/              |

#### Setup
##### Clone Repository
In an appropriate folder, run the following commands:
```shell
> git clone https://github.com/ibuttimer/in-for-a-penny.git
> cd in-for-a-penny
```
Alternatively, most IDEs provide an option to create a project from Version Control.

#### Virtual Environment
It is recommended that a virtual environment be used for development purposes.
Please see [Creating a virtual environment](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/#creating-a-virtual-environment) for details.

> __Note:__ Make sure to [activate the virtual environment](https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/#activating-a-virtual-environment).

#### Python Setup
In the `in-for-a-penny` folder, run the following command to install the necessary python packages:
```shell
> pip install -r requirements-dev.txt
```
##### Production versus Development Setup
There are two requirements files:
* [requirements.txt](requirements.txt) which installs the production requirements, and
* [requirements-dev.txt](requirements-dev.txt) which installs extra development-only requirements in addition to the production requirements from [requirements.txt](requirements.txt)

###### Table 1: Configuration settings
| Key                      | Value                                                                                                                                                                                                                                                                                           |
|--------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| ENV_FILE                 | If using an environment file, specifies the file to use. Defaults to `.env` in the project root folder.                                                                                                                                                                                         |
| PORT                     | Port application is served on; default 8000                                                                                                                                                                                                                                                     |
| DEBUG                    | A boolean that turns on/off debug mode; set to any of 'true', 'on', 'ok', 'y', 'yes', '1' to enable                                                                                                                                                                                             |
| DEVELOPMENT              | A boolean that turns on/off development mode; set to any of 'true', 'on', 'ok', 'y', 'yes', '1' to enable                                                                                                                                                                                       |
| TEST                     | A boolean that turns on/off test mode; set to any of 'true', 'on', 'ok', 'y', 'yes', '1' to enable. Only valid when development mode is enabled.                                                                                                                                                |
| SECRET_KEY               | [Secret key](https://docs.djangoproject.com/en/4.1/ref/settings/#std-setting-SECRET_KEY) for a particular Django installation. See [Secret Key Generation](#secret-key-generation)                                                                                                              |
| DATABASE_URL             | [Database url](https://docs.djangoproject.com/en/4.1/ref/settings/#databases)                                                                                                                                                                                                                   |
| CLOUDINARY_URL           | [Cloudinary url](https://pypi.org/project/dj3-cloudinary-storage/)                                                                                                                                                                                                                              |
| SITE_ID                  | Id (primary key) of site in the `django_site` table of the database. See [Configure authentication](#configure-authentication).                                                                                                                                                                 |
| HEROKU_HOSTNAME          | [Hostname](https://docs.djangoproject.com/en/4.1/ref/settings/#allowed-hosts) of application on Heroku.<br>__Note:__ To specify multiple hosts, use a comma-separated list with no spaces.<br>__Note:__ Set to `localhost,127.0.0.1` in local development mode                                  |
| REMOTE_DATABASE_URL      | Url of remote PostgreSQL database resource. For an [ElephantSQL](https://www.elephantsql.com/) database this is available from `URL` in the instance details.<br>__Note:__ Only required for admin purposes, see database configuration under [Cloud-based Deployment](#cloud-based-deployment) |

#### Environment variables
Set environment variables corresponding to the keys in [Table 1: Configuration settings](#table-1-configuration-settings).

E.g.
```shell
For Linux and Mac:                       For Windows:
$ export DEVELOPMENT=true                > set DEVELOPMENT=true
```

##### Secret Key Generation
A convenient method of generating a secret key is to run the following command and copy its output.

```shell
$ python -c "import secrets; print(secrets.token_urlsafe())"
```

### Before first run
Before running the application for the first time following cloning from the repository and setting up a new database,
the following steps must be performed, from a terminal window, in the `in-for-a-penny` folder.

#### Initialise the database
````shell
$ python manage.py migrate
````

#### Create a superuser
Enter `Username`, `Password` and optionally `Email address`.
````shell
$ python manage.py createsuperuser
````

#### Configure authentication
From [django-allauth Post-Installation](https://django-allauth.readthedocs.io/en/latest/installation.html#post-installation)
- Add a Site for your domain in the database
  - Login to `http://&lt;domain&gt;/admin/sites/site/` as the previously created superuser, e.g. http://127.0.0.1:8000/admin/sites/site/
  - Add a Site for your domain (django.contrib.sites app) or edit the default entry `example.com`.

    E.g.

    | Domain name | Display name |
    |-------------|--------------| 
    | localhost   | localhost    | 

    __Note:__ The id (primary key) of the site must be added to the application configuration. See `SITE_ID` in [Table 1: Configuration settings](#table-1-configuration-settings).

### Run server
In order to run the development server, run the following command from the `in-for-a-penny` folder:

````shell
$ python manage.py runserver
````

By default, the server runs on port 8000 on the IP address 127.0.0.1.
See [runserver](https://docs.djangoproject.com/en/4.1/ref/django-admin/#runserver) for details on passing an IP address and port number explicitly.

### Cloud-based Deployment

The site was deployed on [Heroku](https://www.heroku.com).



### Deployment
The following steps were followed to deploy the website:
- Login to Heroku in a browser
- From the dashboard select `New -> Create new app`
- Set the value for `App name`, choose the appropriate region and click `Create app`
- To provision the application with a database, such as an [ElephantSQL](https://www.elephantsql.com/) database.
  - For an [ElephantSQL](https://www.elephantsql.com/) database, follow the `Create a new instance` instructions under the `Getting started` section of the [ElephantSQL documentation](https://www.elephantsql.com/docs/index.html).
- From the app settings, select the `Resources` tab.
  - Under `Add-ons` add the following
    1. `Cloudinary - Image and Video Management` - [Cloudinary Image & Video Tools](https://elements.heroku.com/addons/cloudinary)

       __Note:__ In order the access the dashboard for the provisioned Cloudinary account, use the [Heroku CLI](https://devcenter.heroku.com/articles/cloudinary#management-console)
          ```shell
          $ heroku addons:open cloudinary --app=in-for-a-penny
          ```

- From the app settings, select the `Settings` tab.
  - Under `Buildpacks` add the following buildpacks
    1. `heroku/python`
  - Under `Config Vars` add the following environment variables

    | Key                | Value                                                                                                                                                                                       |
    |--------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | PORT               | 8000                                                                                                                                                                                        |
    | SECRET_KEY         | [Secret key](https://docs.djangoproject.com/en/4.1/ref/settings/#std-setting-SECRET_KEY) for a particular Django installation                                                               |
    | HEROKU_HOSTNAME    | [Hostname](https://docs.djangoproject.com/en/4.1/ref/settings/#allowed-hosts) of application on Heroku                                                                                      |
    | SITE_ID            | Id (primary key) of site in the `django_site` table of the database. See [Configure authentication](#configure-authentication).                                                             |
    |                    | _The following keys are automatically added when `Resources` are provisioned:_                                                                                                              |
    | CLOUDINARY_URL     | [Cloudinary url](https://pypi.org/project/dj3-cloudinary-storage/)                                                                                                                          |
    | DATABASE_URL       | [Database url](https://docs.djangoproject.com/en/4.1/ref/settings/#databases)<br>- [ElephantSQL](https://www.elephantsql.com/) database, copy the `URL` from the instance details page |


See [Table 1: Configuration settings](#table-1-configuration-settings) for details.

If any other settings vary from the defaults outlined in [Table 1: Configuration settings](#table-1-configuration-settings) they must be added as well.

- From the app settings, select the `Deploy` tab.
  - For the `Deployment method`, select `GitHub` and link the Heroku app to the GitHub repository.

    __Note:__ To configure GitHub integration, you have to authenticate with GitHub. You only have to do this once per Heroku account. See [GitHub Integration (Heroku GitHub Deploys)](https://devcenter.heroku.com/articles/github-integration).
  - `Enable Automatic Deploys` under `Automatic deploys` to enable automatic deploys from GitHub following a GitHub push if desired.
  - The application may also be deployed manually using `Deploy Branch` under `Manual deploy`

- Initialise the database and Create a superuser

  Involves the same procedure as outlined in [Initialise the database](#initialise-the-database) and [Create a superuser](#create-a-superuser)
  but may be run from the local machine.
  - From a [Development and Local Deployment](#development-and-local-deployment)
    - Initialise the database
      ````shell
      $ python manage.py migrate --database=remote
      ````
    - Create a superuser

      Enter `Username`, `Password` and optionally `Email address`.
      ````shell
      $ python manage.py createsuperuser --database=remote
      ````

    __Note:__ Ensure to specify the `--database=remote` option to apply the change to the database specified by the `REMOTE_DATABASE_URL` environment variable.

  - Alternatively, the [Heroku CLI](#heroku-cli) may be utilised.

    After logging into the Heroku CLI in a terminal window, in the `in-for-a-penny` folder:
    - Initialise the database
      ````shell
      $  heroku run python manage.py migrate --app in-for-a-penny
      ````
    - Create a superuser

      Enter `Username`, `Password` and optionally `Email address`.
      ````shell
      $ heroku run python manage.py createsuperuser --app in-for-a-penny
      ````
- Configure authentication

  Follow the same procedure as outlined in [Configure authentication](#configure-authentication) using the
  Heroku domain as `&lt;domain&gt;`, e.g. `in-for-a-penny.herokuapp.com`

The live website is available at [https://in-for-a-penny.herokuapp.com/](https://in-for-a-penny.herokuapp.com/)











## Testing
<< detail testing logs here - any known bugs, and squashed bugs 🐛🐛 >>

## Credits

### Code
<< any and all code that isn't yours...must go here >>

### Content
<< any content, such as facts/references/text that isn't yours...must go here >>

### Media
<< you may have already done this above in the Imagery section, but just in case, please attribute Media acquisition here >>

### Acknowledgements
<< personal thanks and praise 🙌 >>
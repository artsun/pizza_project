# pizza_project
Manageable pizza delivery service

#### Description:
- pizza **Flavors** and **Sizes** could be managed via **/admin/**;
- based on **Flavors** and **Sizes** **/admin/** create **Pizza** and compose menu;
- menu available via **/api/menu/**;
- based on menu **Customer** can make **Order**;

Customer consists of:

    | Name  | Email | Address |

- **Customer** orders via **/api/orders/**;
- order should contain Pizza from Menu with number specified (see **Queries**);
- order could be changed **/api/orders/-id-/** using Patch HTTP-method;
- to remove specific **Pizza** during update set `number: 0`;
- not available to remove  all **Pizzas**, so to remove Order use delete;
- **Customer** with same email can create different orders, or update name/address;
- to view/change status use **/api/orders/-id-/status**;
- to filter by status use `/api/orders/?status__val=`;
- to filter by name use `/api/orders/?customer__name=`;
- there are 4 type of statuses and changes available only for two first:
  - New
  - In Progress
  - In Delivery
  - Finished
- status names could be customised;
- application designed on future scaling basis: just add ManyToMany Relation in between Pizza - Product;
- there is short Dashboard in django admin;

#### How to run:
- docker-compose build
- docker-compose up (to make all initial db migrations)
- stop Ctrl+C
- optional: to load initial statuses, pizza and sizes:
  - docker-compose run web /usr/local/bin/python manage.py loaddata ../market.json
  - docker-compose run web /usr/local/bin/python manage.py loaddata ../service.json
- docker-compose run web /usr/local/bin/python manage.py createsuperuser
- docker-compose run web /usr/local/bin/python manage.py collectstatic
- docker-compose up

#### Queries
- short [Swagger](https://editor.swagger.io/) description for Order creation in **quieries/openapi.yaml**;
- examples in **./quieries**;
- there is dev server at your service.

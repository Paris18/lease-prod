# lease-product
   This System is a Software Solution for renting system(B2C),customer as the end-user he can rent the product. This Application can maintain the good track of the rented products , also works better communication medium between the vendor and user, it also has the  rating option for product and from this option vendor can  maximize product subscription , good communication track with user.\
   As Further we can automate the payment process and as its centralised system we can easily setup the new business or new branch.

# Installation and Execution
#### Basic Requirements

	Python 3
	Virtualenv

#### step 1: create environment with virtualenv

#### step 2: install the requirements with requirements.txt file located in project folder

       pip install -r requirements.txt
       
#### step 3: Create migration file with makemigration command

      python manage.py makemigrations

#### step 4:apply the migrations to db with migrate command
    
     python manage.py migrate
     
#### step 5:run the application

     python manage.py runserver
   
## Response Sample
 ### Rate the product
 
	curl -X POST \
	  http://127.0.0.1:8000/api/v1/rate_product/rateproduct/ 
	  -H 'Content-Type: application/json' 
	  -d '{
		 "rate": 5,
		 "feedback":"test",
		 "product":"furniture 5",
		 “subscription_id”:’1e04a834-5fec-4f53-9fd3-4a55062de5b5’
	 }'
 #### Note: we assumed that this is valid rent subscription, authorised user

    Response:
    {"status":"Successfully rated Product"}

### List the rates

  	curl -X GET \
  	http://127.0.0.1:8000/api/v1/rate_product/ratelist/ 
  	-H 'Content-Type: application/json'

	Response:
	    {
	    "count": 26,
	    "next": "http://127.0.0.1:8000/api/v1/rate_product/ratelist/?page=2",
	    "previous": null,
	    "results": [
		{
		    "id": "1e04a834-5fec-4f53-9fd3-4a55062de5b5",
		    "created_at": "2019-12-10T11:26:59+0000",
		    "updated_at": "2019-12-10T11:26:59+0000",
		    "is_active": true,
		    "rate": 1,
		    "feedback": "test",
		    "product": "furniture 1",
		    "subscription_id": "88885ed2-b028-4680-b728-6068636c4433"
		},
		.
		.
	      ]
	   }
        # Note: used pagination here and we can filter data by sending 'product' as param(optional)
### Get individual rate details
	
	curl -X GET \
       'http://127.0.0.1:8000/api/v1/rate_product/getrate/?id=1e04a834-5fec-4f53-9fd3-4a55062de5b5'

        Response:
        {
            "id": "1e04a834-5fec-4f53-9fd3-4a55062de5b5",
            "created_at": "2019-12-10T11:26:59+0000",
            "updated_at": "2019-12-10T11:26:59+0000",
            "is_active": true,
            "rate": 1,
            "feedback": "test",
            "product": "furniture 1",
            "subscription_id": "88885ed2-b028-4680-b728-6068636c4433"
        }
### Get all product rate analysis

	curl -X GET \
	http://127.0.0.1:8000/api/v1/rate_product/rates/

	    Response:

	    [
		{
		    "product": "furniture 1",
		    "avg_rate": 3.0,
		    "max_rate": 5,
		    "min_rate": 1,
		    "no_of_rates": 5
		},
	    …
	    ]



### Get individual product rate

	   curl -X GET \
	  'http://127.0.0.1:8000/api/v1/rate_product/product_rate/?product=furniture%201'

	    Response:
	    [
		{
		    "product": "furniture 1",
		    "avg_rate": 3.0,
		    "max_rate": 5,
		    "min_rate": 1,
		    "no_of_rates": 5
		}
	    ]

### Update Rate data

	curl -X PUT \
  	http://127.0.0.1:8000/api/v1/rate_product/updaterate/ \
  	-H 'Content-Type: application/json' \
  	-d '{
		 "rate": 1,
                 "feedback":"update test",
		 "id":"f39e5cda-21d5-4831-a333-42eefcbf6928"
 	}'

    Response:
    {
		 "rate": 1,
         	 "feedback":"update test",
		 "id":"f39e5cda-21d5-4831-a333-42eefcbf6928"
 	}

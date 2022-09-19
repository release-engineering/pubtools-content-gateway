CGW Client Module
========================


Content Gateway REST API Services
**************************************

In order to optimize the deployment of new files REST user interface was added to manipulate the products from a command line. All those endpoints require basic authentication and only accounts with permission to see the content in DM can use GET requests and only users with edit permissions can use DELETE, PUSH or POST endpoints. If you need either of these permissions send a request to help@jboss.org.

Return values 401 (for invalid credentials) and 403 (valid credentials but lack of permissions) are returned by all the functions listed here. Requests, that do changes lock the whole product for all users but you. In case you are trying to modify a product locked by someone else, you get 409 return value.


---------------------------------

cgw_client module reference
******************************

.. automodule:: pubtools._content_gateway.cgw_client
   :members: CGWClient
   :show-inheritance:
   :noindex:



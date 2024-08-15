<h3>Click here for live demo <a href=""https://ecom-production-735b.up.railway.app/>LIVE DEMO</a></h3>
<hr>
<h1>About the project</h1>
<img src='https://github.com/user-attachments/assets/bb85da16-8317-4916-8139-f2d22ec76c7d'>

<p>This is a e-commerce website built with Django</p>

<h3>The common functionalities are:</h3>
<ul>
<li>Users can register and login</li>
<li>Users can add products to their cart (No need to be logged in)</li>
<li>Users can see the description of the products</li>
<li>Users can place their order without creating an account</li>
<li>The admin can see all orders, including shipping address and products</li>
</ul>

<h1>Languages and technologies

<h3>Frontend</h3>
<ul>
  <li>HTML</li>
  <li>CSS</li>
  <li>JavaScript</li>
  <li>Bootstrap</li>
</ul>

<h3>Backend</h3>
<ul>
  <li>Python</li>
  <li>Django</li>
  <li>SQLite3</li>
  
</ul>

<h1>To run project</h1>

<ol>
  <li> Go to ecom/ecom/setting.py</li>
  <ul>
    <li>Comment out or delete line ALLOWED_HOSTS</li>
    <li> Comment out or delete lineCSRF_TRUSTED_ORIGINS</li>
    <li> Go to DATABASES</li>
    <li>Delete or comment out everything EXCEPT first two lines (ENGINE and NAME)</li>
  </ul>
  <li>Go to the directory ecom/ecom</li>
  <li>Run <code>python manage.py runserver</code></li>
</ol>

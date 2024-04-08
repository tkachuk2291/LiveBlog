# Live Blog Project

A cozy blog where everyone can post their own post,
as well as comment and like the posts of other users!


## Installing / Getting started

> 👉 Download the code  

```shell
git clone https://github.com/tkachuk2291/LiveBlog.git
cd LiveBlog
```

<br />

> 👉 Install modules via `VENV`  

```shell
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

<br />

> 👉 Set Up Database

```shell
python manage.py makemigrations
python manage.py migrate
```

<br />

> 👉 Create the Superuser

```shell
python manage.py createsuperuser 
```
```
Or login with default SuperUser:  
Login: Author
Password: Authortest2291
```
<br />

> 👉 Start the app

```shell
 python manage.py runserver
```

At this point, the app runs at `http://127.0.0.1:8000/`. 

<br />


## Features

**Navigation bar and footer**

➜ **Live Blog:**  
Logo and link leading to the main blog page.  

➜**Home page**:   
Section leading to the home page.  

➜**Blog**:   
Section leading to the posts dashboard page.  

➜**About us**:  
Blog info page (in development).  

➜**Dropdown menu + picture**:   
Show profile picture as well as blog and account menus.  

➜**Search**:   
Search box for easy filtering of posts.  

➜**Blog menu**:  
- **Dashboard**: Page where you can view all posts.  
- **Write a new post**: Page where you can create a new post.  
- **My Posts**: A page where you can view all posts and delete or edit them.  

➜**Accounts in navigation**:  
- **My Profile**: Page where you can view and edit your profile.  
- **Change password**: Page to change your password.  
- **Sign out**: Option to log out of the account.  

➜**Search and Pagination**:  
- **Paginate**: Feature that allows you to switch between pages, available in Dashboard, My posts, Comments.  
- **Search**: For convenience, a search bar has been added to the navigation that filters posts by title and users.  

➜**Registration and Authentication**:  
- **Sign up**: Page to register new users where they can create an account and add a photo to their profile.  
- **Forgot password**: Page that allows you to reset your password by email address.  
- **Sign in**: Page to sign in to your account.  

➜**Dashboard & Detail page**:  
- **Dashboard**: This page displays all posts created by users.  
- **Detail page**: Each post has a detail page.  

➜**Comments & Likes & Views & Useful Article**:  
- **Comments**: Available in detail view of each post where any authorized user can leave a comment.  
- **Likes**: Are available on both the Dashboard page and the detail page of each post. Clicking on a heart changes the color and adds a like, it can also be removed.  
- **Views**: A feature that counts the number of times a post has been viewed.  
- **Useful article**: Available only on the post's detail page, a section that encourages readers to view more useful articles.  

➜**Home Page**:  
- **Home Page**: Home page, to which small statistics have been added: number of likes, number of blog posts and number of views over time.  

➜**Other**:  
- **Authentication Check**: Check if the user is logged in. If not, the user will be redirected to the login page.  
- **Dashboard Post & Comments & My posts check**: Check if comments or posts have been created. If not, the "Create Comments" button will be displayed in the comments section.  
- **Display pagination**: If there are no posts or comments, pagination will not be displayed.  
- **Photo system**: Available on every page so that users can upload a photo for a post, for their profile and optionally edit it.  


## Contributing

If you're interested in contributing, simply fork the repository and create a feature branch.  
We appreciate all contributions and warmly welcome pull requests.  

## Links

- Repository: https://github.com/tkachuk2291/LiveBlog.git
- Issue tracker: https://github.com/tkachuk2291/LiveBlog/issues
  - In case of sensitive bugs like security vulnerabilities, please contact
    tkacuk2291@gmail.com directly instead of using issue tracker. We value your effort
    to improve the security and privacy of this project!

  
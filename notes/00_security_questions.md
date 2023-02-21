# Security Questions

## `redirect_authenticated_user = True`

* Warning:

    ![image](https://user-images.githubusercontent.com/47562501/220292242-f2d326e3-23de-4a9d-86e7-d3b0f7afca22.png)

* [`accounts/views.py`](../accounts/views.py)

    ```python
    class CustomLoginView(LoginView):
        #...
        # TODO: Is this functionality a security risk?
        redirect_authenticated_user = True
        #...
    ```

* [`accounts/tests/test_accounts_views.py`](../accounts/tests/test_accounts_views.py)

    ```python
    class CustomLoginViewTest(TestCase):
        #...
        def test_login_view_redirects_to_home_if_user_is_authenticated(self):
            """
            Test that the login view redirects to the home if the user is
            authenticated.

            TODO: Is this functionality in `accounts/views.py` a security risk?
            """
            # Create a user.
            CustomUser.objects.create_user(
                username=USERNAME_REGISTRATION_ACCEPTED_FALSE,
                password=PASSWORD_FOR_TESTING,
            )
            # Log in the user.
            self.client.login(
                username=USERNAME_REGISTRATION_ACCEPTED_FALSE,
                password=PASSWORD_FOR_TESTING,
            )
            # Test that the login view redirects to home if the user is
            # authenticated.
            response = self.client.get(LOGIN_URL)
            self.assertRedirects(response, HOME_URL)
        #...
    ```

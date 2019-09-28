import React from 'react';
import { createAppContainer } from
'react-navigation';
import { createStackNavigator } from 'react-navigation-stack'
import Home from './Pages/Home';
import LoginPage from './Pages/LoginPage';
import RegisterPage from './Pages/RegisterPage';
import { Provider } from 'mobx-react';
import Store from './Classes/store'


class App extends React.Component{
  render(){
    return(
      <Provider rootStore = {Store}>
        <AppContainer />        
      </Provider>
    )
  }
}

const AppNavigator = createStackNavigator(
  {
    Home,
    LoginPage,
    RegisterPage
  },
  {
    initialRouteName: 'Home',
  }
);

const AppContainer = createAppContainer(AppNavigator)
export default App;

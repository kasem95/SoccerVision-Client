import React from 'react';
import { View, Button, Text } from 'react-native';

class Home extends React.Component {
    goToLoginPage = () =>{
        this.props.navigation.navigate("LoginPage")
    }

    goToRegisterPage = () =>{
        this.props.navigation.navigate("RegisterPage")
    }

    render() {
        return (
            <View>
                <Button 
                    onPress={this.goToLoginPage}
                    title = "Existed account"
                >
                    Existed account
                </Button>
                
                <Button 
                    onPress={this.goToRegisterPage}
                    title = "Create a new account"
                >
                    Create a new account
                </Button>
            </View>
        )
    }
}

export default Home;
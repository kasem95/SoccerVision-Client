import React from 'react';
import { StyleSheet, Text, View, TextInput, Button } from 'react-native';
import { observer, inject } from 'mobx-react';
import User from '../Classes/User'

const Login = props => {

    let user =
    {
        email: null,
        password: null
    }

    const changeEmail = val => {
        user.email = val
    }

    const changePass = val => {
        user.password = val
    }

    login = () => {

        console.log(user)
        
        fetch(`http://ruppinmobile.tempdomain.co.il/site09/api/Users/${user.email},${user.password}/login`, {
            method: 'GET',
            headers: new Headers({
                'Content-Type': 'application/json;',
            })
        })
            .then(res => {
                console.log("res=", res);
                return res.json();
            })
            .then(
                result => {
                    console.log("fetch GET= ", result);
                    if (typeof result == "string") {
                        alert(result);
                    } else {
                        //console.log(result)
                        let user = new User(result.UserID,result.Email,result.Password,result.Username,result.IsInMatch,result.MatchID);
                        props.rootStore.insertUser(user);
                        console.log(props.rootStore.user)
                        alert(props.rootStore.user)
                    }
                },
                error => {
                    console.log("=> err post=", error);
                }
            );
    }


    return (
        <View>
            <Text>Login</Text>

            <TextInput
                name="email"
                placeholder="Email"
                onChangeText={val => changeEmail(val)}
            />
            <TextInput
                name="password"
                placeholder="Password"
                onChangeText={val => changePass(val)}
            />

            <Button
                title="Login"
                onPress={login}
            >
                Login
            </Button>
        </View>
    )
}

export default inject('rootStore')(observer(Login))

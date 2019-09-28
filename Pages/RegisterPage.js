import React from 'react';
import { StyleSheet, Text, View, TextInput, Button } from 'react-native';
import { observer, inject } from 'mobx-react';

function Register(props){
    return(
        <View>
            
        </View>
    )
}

export default inject('rootStore')(observer(Register))
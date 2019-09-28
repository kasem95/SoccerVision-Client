import { decorate, observable, action, computed, configure } from 'mobx';


configure({enforceActions:"observed"});

class Store{
    user = null
    matches = [];

    insertUser = val =>{
        this.user = val
    }
}

decorate(Store,{
    user:observable,
    matches:observable,
    insertUser:action
});

export default new Store();
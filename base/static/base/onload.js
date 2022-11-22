var registerLoadFunction;
var _onload_handler;

(()=>{
    let load_functions = [];
    _onload_handler = () => {
        for(let f of load_functions)
            f();
    }

    registerLoadFunction = (func) => {
        load_functions.push(func);
    }
})();
let app = {};

let init = (app) => {
    app.data = {
        message: "buffering...",
        state: "init", 
        right_answer: "",

        board: [],
        players: [],

        lives: 3,
        score: 0,
    };

    app.enumerate = (a) => {
        let k = 0;
        a.map((e) => {e._idx = k++;});
        return a;
    };

    app.post_guess = (guess_) => {
        axios.post(post_guess_url, { guess: [guess_] })
             .then( (result) => {
                 app.get_cards();
                 console.log(`app.post_guess: ${result.data.right_answer}`);
                 console.log(`guess: ${guess_}`);
                 app.vue.right_answer = result.data.right_answer;
                 app.vue.lives = result.data.lives;
                 app.vue.score = result.data.score;
                 if( result.data.is_end ) {
                     setTimeout( () => {
                        app.vue.score = 0;
                        app.vue.lives = 3;
                     }, 5000);
                 }
             });
    };

    app.get_cards = () => {
        axios.get(get_cards_url)
             .then( (result) => {
               console.log(`get_cards: ${result.data.board}`);
               console.log(`get_cards: ${result.data.players}`);
               app.vue.board = app.vue.enumerate(result.data.board);
               app.vue.players = 
                 app.vue.enumerate(result.data.players);
               console.log(`-board: ${app.vue.board}`);
               console.log(`-players: ${app.vue.players}`);
             });
    };

    app.methods = {
        enumerate: app.enumerate,
        post_guess: app.post_guess,
        get_cards: app.get_cards,
    };

    app.vue = new Vue({
        el: "#vue-target",
        data: app.data,
        methods: app.methods
    });

    app.init = () => {
       console.log("initing");
       app.vue.get_cards(); 
    };

    app.init();
};

init(app);


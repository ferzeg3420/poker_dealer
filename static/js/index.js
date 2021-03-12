const MAX_PLAYERS = 9;

let app = {};

let init = (app) => {
    app.data = {
        message: "buffering...",
        state: "init", 
        right_answer: [],

        player_guesses: [],
        right_guesses: [],

        show_cash_increment: false,
        show_lives_decrement: false,

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
               app.vue.board = app.vue.enumerate(result.data.board);
               app.vue.players = 
                 app.vue.enumerate(result.data.players);
             });
    };

    app.add_or_delete_guess(player_number) => {
       if( player_number > 0 && player_number <= players.length ) {
         player_guesses[player_number] = !player_guesses[player_number];
       }
    }

    app.goto_load = () => {
       app.vue.state = "load";
       app.vue.get_cards(); 
       // card-flipping animation goes here
       app.vue.goto_guess();
    };

    // to enable the make veredict button
    app.goto_get_guess = () => {
       app.vue.state = "get_guess";
    };
    
    app.goto_make_guess = () => {
       app.vue.state = "make_guess";
       guess = [];
       for( let i = 1; i <= MAX_PLAYERS ) {
         if( app.vue.player_guesses[i] ) {
           guess.append(i);
         }
       }
       app.vue.post_guess(guess);
       app.vue.goto_compare();
    };
    
    // used to enable the continue button
    // and show -1 to lives or +5 to $
    app.goto_compare = () => {
       app.vue.state = "compare";
       for( let i of app.vue.right_answer ) {
           app.vue.right_guesses[i] = true;
       }
    };

    app.methods = {
        enumerate: app.enumerate,
        post_guess: app.post_guess,
        get_cards: app.get_cards,
        goto_load: app.goto_load, 
        goto_get_guess: app.goto_get_guess, 
        goto_make_guess: app.goto_make_guess, 
        goto_compare: app.goto_compare, 
        add_or_delete_guess: app.add_or_delete_guess,
    };

    app.vue = new Vue({
        el: "#vue-target",
        data: app.data,
        methods: app.methods
    });

    app.init = () => {
       console.log("initing");
       app.vue.player_guesses = [];
       for( let i = 0; i <= MAX_PLAYERS; i++) {
           app.vue.player_guesses.append(false);
       }
       app.vue.goto_load();
    };

    app.init();
};

init(app);


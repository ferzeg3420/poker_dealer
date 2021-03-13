const MAX_PLAYERS = 9;

const LOAD_STATE = "load";
const GET_GUESS_STATE = "get_guess";
const MAKE_GUESS_STATE = "make_guess";
const COMPARE_STATE = "compare";

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
        axios.post(post_guess_url, { guess: guess_ })
             .then( (result) => {
                 console.log(`app.post_guess: ${result.data.right_answer}`);
                 console.log(`guess: ${guess_}`);
                 app.vue.right_answer = result.data.right_answer;
                 app.vue.lives = result.data.lives;
                 app.vue.score = result.data.score;
                 // Delete the stuff below vvv
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

    app.add_or_delete_guess = (player_number) => {
       console.log("start of add or delete guess");
       if( app.vue.state != "get_guess" ) return;
       console.log("add or delete guess after get_guess state check");
       console.log(`---players.length: ${app.vue.players.length}`);
       console.log(`---player number: ${player_number}`);
       if( player_number > 0 
           && player_number <= app.vue.players.length ) {
         //app.vue.player_guesses[player_number] =
         //   !app.vue.player_guesses[player_number];
            Vue.set(app.vue.player_guesses, 
                    player_number,
                    !app.vue.player_guesses[player_number]);
         console.log(`player_guesses: [${app.vue.player_guesses}]`);
       }
    }

    app.goto_load = () => {
       app.vue.state = "load";
       app.vue.get_cards(); 
       // card-flipping animation goes here
       app.vue.goto_get_guess();
    };

    // to enable the make veredict button
    app.goto_get_guess = () => {
       app.vue.state = "get_guess";
    };
    
    app.goto_make_guess = () => {
       app.vue.state = "make_guess";
       guess = [];
       for( let i = 1; i <= MAX_PLAYERS; i++ ) {
         if( app.vue.player_guesses[i] ) {
           guess.push(i);
         }
       }
       // reset the player guesses array once the guesses are saved
       for( let i = 1; i <= MAX_PLAYERS; i++ ) {
         app.vue.player_guesses[i] = false;
       }
       app.vue.post_guess(guess);
       app.vue.goto_compare();
    };
    
    // used to enable the continue button
    // and show -1 to lives or +5 to $
    app.goto_compare = () => {
       // +5 or -1 animation that fades out goes here
       for( let i = 0; i < MAX_PLAYERS; i++ ) {
           app.vue.right_guesses[i] = false;
       }
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
           app.vue.player_guesses.push(false);
       }
       // load live and money info
       axios.get(get_init_game_state_url)
            .then( (result) => {
                app.vue.lives = result.data.lives;
                app.vue.score = result.data.running_score;
            });
       app.vue.goto_load();
    };

    app.init();
};

init(app);


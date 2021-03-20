const MAX_PLAYERS = 9;

const LOAD_STATE = "load";
const GET_GUESS_STATE = "get_guess";
const MAKE_GUESS_STATE = "make_guess";
const COMPARE_STATE = "compare";

let app = {};

let init = (app) => {
    app.data = {
        message: "Three of a Kind",
        state: "init", 
        right_answer: [],
        is_end: false,
        name_input: "",
        time: "",

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
                 if( result.data.lives < app.vue.lives ) {
                     app.vue.show_lives_decrement = true;
                 }
                 else {
                     app.vue.show_cash_increment = true;
                 }
                 app.vue.is_end = result.data.is_end;
                 app.vue.right_answer = result.data.right_answer;
                 app.vue.lives = result.data.lives;
                 app.vue.score = result.data.score;
             });
    };

    app.score_to_leaderboard = () => {
        if( app.vue.state !== "score_save" ) {
            return;
        }
        let name_ = app.vue.name_input; 
        axios.post(score_to_leaderboard_url, { name: name_ })
             .then( (result) => {
                  app.vue.time = result.data.time;
             });
        app.vue.close_score_save();
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
       if( app.vue.state != "get_guess" ) return;
       if( player_number > 0 
           && player_number <= app.vue.players.length ) {
            Vue.set(app.vue.player_guesses, 
                    player_number,
                    !app.vue.player_guesses[player_number]);
       }
    }

    app.close_score_save = () => {
        let save_score_modal = 
            document.getElementById("save-score-modal");
        save_score_modal.style.display = "none";
        app.vue.goto_load();
    };

    app.goto_score_save = () => {
        app.vue.message = "Well done!";
        app.vue.state = "score_save";
        app.vue.get_game_time();
        let save_score_modal = 
            document.getElementById("save-score-modal");
        save_score_modal.style.display = "block";
    };

    app.goto_load = () => {
       app.vue.state = "load";
       app.vue.message = "Shuffling the deck";
       app.vue.show_lives_decrement = false;
       app.vue.show_cash_increment = false;
       // load live and money info
       axios.get(get_init_game_state_url)
            .then( (result) => {
                app.vue.lives = result.data.lives;
                app.vue.score = result.data.running_score;
            });

       app.vue.get_cards(); 
       // card-flipping animation goes here
       app.vue.goto_get_guess();
    };

    // to enable the make veredict button
    app.goto_get_guess = () => {
       app.vue.message = "Choose the best hands";
       app.vue.state = "get_guess";
    };

    app.get_game_time = () => {
       axios.get(get_game_time_url)
            .then( (result) => {
                app.vue.time = result.data.time;
            });
    };
    
    app.goto_make_guess = () => {
       app.vue.message = "Manager is checking";
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
       app.vue.message = "Three of a kind";
       // +5 or -1 animation that fades out goes here
       for( let i = 0; i < MAX_PLAYERS; i++ ) {
           app.vue.right_guesses[i] = false;
       }
       app.vue.state = "compare";
       for( let i of app.vue.right_answer ) {
           app.vue.right_guesses[i] = true;
       }
    };

    app.resolve_compare = () => {
      if( app.vue.is_end ) {
          app.vue.goto_score_save();
      }
      else {
          app.vue.goto_load();
      }
    }

    app.methods = {
        enumerate: app.enumerate,
        post_guess: app.post_guess,
        get_cards: app.get_cards,
        score_to_leaderboard: app.score_to_leaderboard,
        goto_load: app.goto_load, 
        goto_get_guess: app.goto_get_guess, 
        goto_make_guess: app.goto_make_guess, 
        goto_compare: app.goto_compare, 
        add_or_delete_guess: app.add_or_delete_guess,
        close_score_save: app.close_score_save, 
        goto_score_save: app.goto_score_save, 
        resolve_compare: app.resolve_compare, 
        get_game_time: app.get_game_time,
    };

    app.vue = new Vue({
        el: "#vue-target",
        data: app.data,
        methods: app.methods
    });

    app.init = () => {
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


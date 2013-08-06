// Models
window.Gift = Backbone.Model.extend({
    urlRoot:"../get_gifts/",
    defaults:{
        "id":null,
        "title":"",
        "description":"",
        "number":null,
        "booker":"",
    }    
});

window.GiftCollection = Backbone.Collection.extend({
    model:Gift,
    url:"../get_gifts/"
});


// Views
window.GiftListView = Backbone.View.extend({
 
    tagName:'div',
 
    initialize:function () {
        this.model.bind("reset", this.render, this);
    },
 
    render:function (eventName) {
        _.each(this.model.models, function (gift) {
            $(this.el).append(new GiftListItemView({model:gift}).render().el);
        }, this);
        return this;
    }
 
});

window.GiftListItemView = Backbone.View.extend({

    tagName:"div",

    template:_.template($('#gift_listing').html()),
    
    initialize:function () {
        this.model.bind("change", this.render, this);        
    },
    
    render: function (eventName) {
            $(this.el).html(this.template(this.model.toJSON()));
        return this;    
    },

   events:{
        "click .save":"saveGift",
    },
 
    saveGift:function () {
        if (this.model.get('booker') === 'mine'){
            this.model.set({
                booker:"",
            });   
        }
        else {
            this.model.set({
                booker:'mine',
            });
        }
        function readCookie(name) {
            var nameEQ = name + "=";
            var ca = document.cookie.split(';');
            for(var i=0;i < ca.length;i++) {
                var c = ca[i];
                while (c.charAt(0)==' ') c = c.substring(1,c.length);
                if (c.indexOf(nameEQ) == 0) return c.substring(nameEQ.length,c.length);
            }
            return null;
        }       
        $.ajaxSetup({
            beforeSend: function(jqXHR){
                jqXHR.setRequestHeader("X-CSRFToken", readCookie('csrftoken'));
            }
        });
        this.model.save();
        return false;
    },

    close:function () {
        $(this.el).unbind();
        $(this.el).empty();
    }
 });

// Router
var AppRouter = Backbone.Router.extend({

    routes:{
        "":"list",
    },

    list: function () {
        this.giftList = new GiftCollection();
        this.giftListView = new GiftListView({model:this.giftList});
        var that = this;
        this.giftList.fetch({success:  function(a) {
            $('#gift_container').html(that.giftListView.render().el);
        },
        });
    },
});

var app = new AppRouter();
Backbone.history.start();

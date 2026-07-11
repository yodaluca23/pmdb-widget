# Public Meta DataBase Discord Widget

> ⚠️ **Very Early Beta**

## How to Setup

Thanks to [Chloe Cinder's Guide](https://chloecinders.com/blog/discord-widgets).

1. Open the [Discord Developer Portal](https://discord.com/developers/applications)
2. Create a new application
3. Go to **Games > Social SDK** and apply for Social SDK access
4. Run this snippet in your browser console to gain access to the widget experiment:

```javascript
let _mods = webpackChunkdiscord_developers.push([[Symbol()],{},r=>r.c]);
webpackChunkdiscord_developers.pop();

let findByProps = (...props) => {
    for (let m of Object.values(_mods)) {
        try {
            if (!m.exports || m.exports === window) continue;
            if (props.every((x) => m.exports?.[x])) return m.exports;

            for (let ex in m.exports) {
                if (props.every((x) => m.exports?.[ex]?.[x]) && m.exports[ex][Symbol.toStringTag] !== 'IntlMessagesProxy') return m.exports[ex];
            }
        } catch {}
    }
}

findByProps("getAll").getAll().find(e=>e.getName() === "ApexExperimentStore").createOverride("2026-03-widget-config-editor", 1)
```

5. Copy the contents of `config.json`
6. Paste it into the widget editor with the three dot menu in the top right
7. Fill in the images with whatever you want
8. Save and publish
9. Setup OAuth with any redirect with the `openid` and `sdk.social_layer` permissions
   - Change `response_type=code` to `response_type=token`
10. Authorize your account
11. Copy `.env.example` to `.env` and fill in all the details
12. Run this snippet in the Discord app console to add the widget to your profile:

```javascript
let _mods=webpackChunkdiscord_app.push([[Symbol()],{},e=>e.c]);webpackChunkdiscord_app.pop();
let findByProps=(...e)=>{for(let t of Object.values(_mods))try{if(!t.exports||t.exports===window)continue;if(e.every(e=>t.exports?.[e]))return t.exports;for(let r in t.exports)if(e.every(e=>t.exports?.[r]?.[e])&&"IntlMessagesProxy"!==t.exports[r][Symbol.toStringTag])return t.exports[r]}catch{}};

api = findByProps("Bo", "Cu").Bo
async function addWidget(appId) {
    id = findByProps("getCurrentUser").getCurrentUser().id;
    current_widgets = (await api.get("/users/" + id + "/profile")).body.widgets
    if (current_widgets.map(x=>x.data?.application_id).includes(appId)) {return console.log("Already in your widgets — remove it via Discord client to re-add")}
    current_widgets.unshift({"data": {"type": "application","application_id": appId}})
    await api.put({url: "/users/@me/widgets",body:{widgets: current_widgets}})
}
// Usage
addWidget("<APPLICATION_ID>")
```

13. Run `main.py` — it will update your widget every 15 seconds while it's running
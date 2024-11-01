// Define regular expressions to match both types of keys
const keyPattern1 = /.*?-login\.windows\.net-accesstoken-.*?-https:\/\/groupssvc\.fl\.teams\.microsoft\.com\/teams\.readwrite--/;
const keyPattern2 = /login\.windows\.net-accesstoken.*service::api\.fl\.teams\.microsoft\.com/;

let key1Secret = null; // For MESSAGE_TOKEN
let key2Secret = null; // For SEARCH_TOKEN
var parsedValue;
// Loop through all keys in local storage
for (let i = 0; i < localStorage.length; i++) {
    const key = localStorage.key(i);
    let value = localStorage.getItem(key);
            
    // Check if the current key matches the pattern for Key 2 (Skype access / SEARCH_TOKEN)
    if (keyPattern2.test(key)) {
        parsedValue = JSON.parse(value);
        if (parsedValue && parsedValue.secret) {
            key2Secret = parsedValue.secret;
        }
    }

    // Check if the current key matches the pattern for Key 1 (Teams access / MESSAGE_TOKEN)
    if (keyPattern1.test(key)) {
        parsedValue = JSON.parse(value);
        if (parsedValue && parsedValue.secret) {
            key1Secret = parsedValue.secret;
        }
    }
}

// Print the secrets in the desired order

if (key2Secret) {
    console.log(`SEARCH_TOKEN=${key2Secret}`);
} else {
    console.log("SEARCH_TOKEN not found.");
}

if (key1Secret) {
    console.log(`MESSAGE_TOKEN=${key1Secret}`);
} else {
    console.log("MESSAGE_TOKEN not found.");
}

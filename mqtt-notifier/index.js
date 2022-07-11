const mqtt = require('mqtt')
const notifier = require('node-notifier')

const config = require('config')

const log = console.log

function showNotification(title, message) {
    notifier.notify({
        title,
        message
    })
}

function main() {
    log(config.get('mqtt'))
    const client = mqtt.connect({...config.get('mqtt')})
    const {userId: tgUserId} = config.get('telegram')
    const topic = 'toggle/101'

    log("connecting...")
    client.on('connect', () => {
        log("Connected")
        client.subscribe(`${tgUserId}/${topic}`)
    })
    client.on('error', e => console.log(e))
    client.on('message', (topic, message) => {
        topic = topic.substr(tgUserId.length + 1)
        message = message.toString()
        log(`[${topic}] ${message}`)
        showNotification(topic, message)
    })
}

main()

import mqtt from 'mqtt'
import config from 'config'
import {me, startTimeTracking, stopTimeTracking} from './toggl-track-client.js'

const log = console.log

const workspaceId = 224075;
const projectIds = {
    busy: 184161602,
    idle: 184161606
}

async function switchTask(projectId, description) {
    await stopTimeTracking()
    await startTimeTracking(workspaceId, projectId, description)
}

async function handleMqttMessage(message) {
    log(message)
    if (message.startsWith('[busy]')) {
        await switchTask(projectIds.busy, `Now I'm busy: ${message}`)
    } else if (message.startsWith('[idle]')) {
        await switchTask(projectIds.idle, `Now I'm idle: ${message}`)
    }
}

async function main() {
    const client = mqtt.connect({...config.get('mqtt')})
    const {userId: tgUserId} = config.get('telegram')
    const topic = 'toggle/101'

    log("Connecting to MQTT...")

    client.on('connect', () => {
        log("Connected")
        client.subscribe(`${tgUserId}/${topic}`)
    })

    client.on('error', e => log(e))
    client.on('message', (_t, m) => handleMqttMessage(m.toString()))
}

main().catch(log)


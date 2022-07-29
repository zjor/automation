import got from 'got'
import config from 'config'

const toggl = config.get('toggl')

const log = console.log

const baseUrl = 'https://api.track.toggl.com/api/v9'
const basicAuthHash = btoa(`${toggl.token}:api_token`)
const options = {
    headers: {
        authorization: `Basic ${basicAuthHash}`,
        'Content-Type': 'application/json'
    }
}

export async function me() {
    return got.get(`${baseUrl}/me`, {...options})
}

export async function getCurrentTimeEntry() {
    return got.get(`${baseUrl}/me/time_entries/current`, {...options})
}

export async function startTimeTracking(workspaceId, projectId, description) {
    const now = new Date().toISOString()
    const json = {
        "created_with": "nodeJS",
        "pid": projectId,
        "tid": null,
        description,
        "tags": [],
        "billable": false,
        "duration": -1658844435,
        "wid": workspaceId,
        "start": now,
        "stop": null,
        "at": now
    }
    return got.post(`${baseUrl}/workspaces/${workspaceId}/time_entries`, {...options, json})
}

export async function stopTimeTracking() {
    const current = JSON.parse((await getCurrentTimeEntry()).body)
    if (!current) {
        console.log("No running tasks")
        return
    }
    console.log(`Stopping ${JSON.stringify(current)}`)


    const { id, workspace_id: workspaceId, start } = current
    const now = new Date()
    const startDate = new Date(start)

    log(`Duration: ${now - startDate}`)

    const json = {
        duration: Math.ceil((now - startDate) / 1000),
        workspace_id: workspaceId
    }

    log(`Payload: ${JSON.stringify(json)}`)

    return got.put(`${baseUrl}/workspaces/${workspaceId}/time_entries/${id}`, {...options, json})
}

async function main() {
    try {
        const workspaceId = 224075;
        const projectId = 163308321;
        const createTaskResponse = await startTimeTracking(workspaceId, projectId, "Hello from NodeJS")
        console.log(createTaskResponse.body)
        const response = await getCurrentTimeEntry()
        console.log(response.statusCode)
        console.log(response.body)

        const stopResponse = await stopTimeTracking()
        log(`HTTP code: ${stopResponse.statusCode}`)
    } catch (e) {
        console.error(`Error: ${e.response.body}`)
    }
}

// main().catch(console.log)

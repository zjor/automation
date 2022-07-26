import got from 'got'
import config from 'config'
const toggl = config.get('toggl')

const baseUrl = 'https://api.track.toggl.com/api/v9'
const basicAuthHash = btoa(`${toggl.token}:api_token`)
const options = {
    headers: {
        authorization: `Basic ${basicAuthHash}`,
        'Content-Type': 'application/json'
    }
}

async function me() {
    return got.get(`${baseUrl}/me`, {...options})
}

async function getCurrentTimeEntry() {
    return got.get(`${baseUrl}/me/time_entries/current`, {...options})
}
/*
{"billable":"boolean",
"created_with":"string",
"description":"string",
"duration":"integer",
"duronly":"boolean",
"pid":"integer",
"postedFields":["string"],
"project_id":"integer",
"start":"string",
"start_date":"string",
"stop":"string",
"tag_action":"string",
"tag_ids":["integer"],
"tags":["string"],
"task_id":"integer",
"tid":"integer",
"uid":"integer",
"user_id":"integer",
"wid":"integer",
"workspace_id":"integer"},
*/

/*
'{"created_with":"API example code","pid":null,"tid":null,"description":"Hello Toggl","tags":[],"billable":false,"duration":-1654686174,"wid":1,"at":"1984-06-08T11:02:53.836Z","start":"1984-06-08T11:02:53.000Z","stop":null}' \
*/

async function startTimeEntry(workspaceId, projectId, description) {
    // const now = new Date().toISOString()
    const now = '2022-07-26T13:05:18+00:00'
    const json = {
        wid: workspaceId,
        workspace_id: workspaceId,
        pid: projectId,
        project_id: projectId,
        created_with: 'IoT-toggle',
        description: description,
        billable: false,
        duration: -1654686174,
        duronly: false,
        at: now,
        start: now,
        stop: null
    }
    return got.post(`${baseUrl}/workspaces/${workspaceId}/time_entries`, {...options, json})
}

async function main() {
    try {
        const workspaceId = 224075;
        const projectId = 163308321;
        const createTaskResponse = await startTimeEntry(workspaceId, projectId, "Hello from NodeJS")
        console.log(createTaskResponse.body)
        const response = await getCurrentTimeEntry()
        console.log(response.statusCode)
        console.log(response.body)
    } catch (e) {
        console.error(`Error: ${e}`)
    }
}

main().catch(console.log)

export interface APIErrorResponse {
    code: number; 
    message: string;
}

const API_URL: string = process.env.CHAT_API_ENDPOINT || 'http://localhost:5000';

export class APIService {

    static isJson(res: Response): boolean {
        return !!res.headers.get('content-type')?.includes('application/json');
    }

    static async do(route: RequestInfo, options: RequestInit) {
        const res = await fetch(route, options);
        await APIService.throwIfError(res);
        if (APIService.isJson(res)) {
            return await res.json();
        }
        return await res.text();
    }

    static async throwIfError(res: Response): Promise<void> {
        if (res.ok) {
            return;
        }
        if (APIService.isJson(res)) {
            throw await res.json();
        }
        const error: APIErrorResponse = { code: res.status, message: res.statusText };
        throw error;
    }

    static async ping(): Promise<string> {
        return APIService.do(`${API_URL}/ping`, {
            method: 'GET',
        });
    }

    static async signIn(username: string): Promise<boolean> {
        return APIService.do(`${API_URL}/user/${username}/signin`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
        });
    }
}

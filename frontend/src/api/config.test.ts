import {
    afterEach,
    describe,
    expect,
    test,
    vi,
} from "vitest";


/*
config.ts reads the environment when it is first imported,
so each test re-imports it after setting the environment.
*/
async function loadApiBaseUrl(): Promise<string> {

    vi.resetModules();

    const config = await import("./config");

    return config.API_BASE_URL;

}


afterEach(() => {
    vi.unstubAllEnvs();
});


describe("API configuration", () => {

    /*
    Verify that the local backend is used when
    VITE_API_BASE_URL is not set.
    */
    test("defaults to the local backend", async () => {

        vi.stubEnv("VITE_API_BASE_URL", undefined);

        expect(
            await loadApiBaseUrl()
        ).toBe("http://localhost:8000");

    });


    /*
    Verify that VITE_API_BASE_URL overrides the default.
    */
    test("uses VITE_API_BASE_URL when it is set", async () => {

        vi.stubEnv("VITE_API_BASE_URL", "http://backend.test:9000");

        expect(
            await loadApiBaseUrl()
        ).toBe("http://backend.test:9000");

    });

});

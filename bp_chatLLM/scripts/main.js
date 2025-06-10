import { world, system } from "@minecraft/server";
import { HttpRequest, HttpRequestMethod, HttpHeader, http } from "@minecraft/server-net";

world.beforeEvents.chatSend.subscribe((eventData) => {
    const player = eventData.sender;
    const message = eventData.message;
    const lowerMessage = message.toLowerCase();

    // Check for Gaben mention
    if (lowerMessage.includes("@gaben")) {
        eventData.cancel = true;
        player.sendMessage("§g[Gaben] Thinking...");
        const request = new HttpRequest("http://localhost:9595/gaben");
        request.method = HttpRequestMethod.Post;
        request.headers = [new HttpHeader("Content-Type", "application/json")];
        request.body = JSON.stringify({
            player: player.name,
            message: message
        });

        system.runTimeout(async () => {
            try {
                const response = await http.request(request);
                if (response.status !== 200) {
                    player.sendMessage(`§c[Gaben] Failed to respond (${response.status})`);
                    return;
                }

                const data = JSON.parse(response.body);
                const reply = data.content || "[Gaben] No response.";

                player.sendMessage(`§b[Gaben] §f${reply}`);
            } catch (err) {
                console.error(err);
                player.sendMessage(`§c[Gaben] Error: ${err}`);
            }
        });

        return;
    }
});

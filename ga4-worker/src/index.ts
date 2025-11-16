// GA4 Proxy Worker – TPS-STAR
// Forward GA4 events (page_view, add_to_cart, checkout, purchase) via Measurement Protocol

export interface Env {
  GA4_MEASUREMENT_ID: string;
  GA4_API_SECRET: string;
}

export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    try {
      const url = new URL(request.url);

      // 1) Event name (default = page_view)
      const eventName = url.searchParams.get("event") || "page_view";

      // 2) Basic page context
      const page_location = url.searchParams.get("location") || "";
      const page_title = url.searchParams.get("title") || "";

      // 3) E-commerce (optionnel)
      const valueRaw = url.searchParams.get("value");
      const currency = url.searchParams.get("currency") || undefined;
      const transaction_id = url.searchParams.get("transaction_id") || undefined;
      const itemsRaw = url.searchParams.get("items");

      let value: number | undefined = undefined;
      if (valueRaw) {
        const parsed = parseFloat(valueRaw);
        if (!Number.isNaN(parsed)) value = parsed;
      }

      let items: any[] | undefined = undefined;
      if (itemsRaw) {
        try {
          items = JSON.parse(itemsRaw);
        } catch (_e) {
          // ignore malformed JSON
        }
      }

      // 4) Client ID (simple UUID, tu pourras plus tard le remplacer par un cookie)
      const clientId = crypto.randomUUID();

      // 5) Construction des params GA4
      const params: Record<string, any> = {
        page_location,
        page_title,
      };

      if (value !== undefined) params.value = value;
      if (currency) params.currency = currency;
      if (transaction_id) params.transaction_id = transaction_id;
      if (items) params.items = items;

      const payload = {
        client_id: clientId,
        events: [
          {
            name: eventName,
            params,
          },
        ],
      };

      const ga4Url =
        `https://www.google-analytics.com/mp/collect?` +
        `measurement_id=${env.GA4_MEASUREMENT_ID}&api_secret=${env.GA4_API_SECRET}`;

      const gaResponse = await fetch(ga4Url, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });

      // On ne renvoie pas la réponse GA4 au frontend (juste un statut OK)
      return new Response(
        JSON.stringify({
          status: "ok",
          forwarded_event: eventName,
        }),
        {
          status: 200,
          headers: { "Content-Type": "application/json" },
        }
      );
    } catch (err) {
      return new Response(
        JSON.stringify({
          error: String(err),
        }),
        {
          status: 500,
          headers: { "Content-Type": "application/json" },
        }
      );
    }
  },
};

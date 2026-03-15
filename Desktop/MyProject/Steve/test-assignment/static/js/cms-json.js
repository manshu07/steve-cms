/**
 * CMS JSON Helpers
 * Utility functions for handling JSON fields in the CMS
 */

(function() {
    'use strict';

    // Safe JSON parse with fallback
    function safeJsonParse(str, fallback) {
        try {
            return JSON.parse(str);
        } catch (e) {
            return fallback;
        }
    }

    // Format JSON for display
    function formatJson(obj) {
        return JSON.stringify(obj, null, 2);
    }

    // Normalize blocks JSON to canonical shape
    function normalizeBlocksJson(value) {
        if (!value) {
            return { blocks: [] };
        }

        // Handle string "null"
        if (typeof value === 'string' && value.toLowerCase() === 'null') {
            return { blocks: [] };
        }

        // Parse if string
        let parsed;
        if (typeof value === 'string') {
            parsed = safeJsonParse(value, { blocks: [] });
        } else {
            parsed = value;
        }

        // If it's a raw array, wrap it
        if (Array.isArray(parsed)) {
            return { blocks: parsed };
        }

        // If it has blocks property, use it
        if (parsed.blocks && Array.isArray(parsed.blocks)) {
            return parsed;
        }

        // Fallback
        return { blocks: [] };
    }

    // Expose helpers globally
    window.cmsJson = {
        safeJsonParse,
        formatJson,
        normalizeBlocksJson
    };

})();

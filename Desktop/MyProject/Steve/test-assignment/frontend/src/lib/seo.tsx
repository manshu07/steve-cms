/**
 * SEO and Metadata management for page builder
 * Handles meta tags, Open Graph, structured data, and social sharing
 */

import React, { memo } from 'react';
import { Helmet } from 'react-helmet-async';
import Typography from '@mui/material/Typography';
import TextField from '@mui/material/TextField';
import { Paper, Box, Grid, Divider, FormControlLabel, Switch } from '@mui/material';

// ============================================================
// TYPES
// ============================================================

export interface SEOMetadata {
  title: string;
  description: string;
  keywords: string;
  ogTitle?: string;
  ogDescription?: string;
  ogImage?: string;
  twitterTitle?: string;
  twitterDescription?: string;
  twitterImage?: string;
  canonicalUrl?: string;
  noIndex?: boolean;
  noFollow?: boolean;
}

export interface StructuredData {
  type: 'WebPage' | 'Article' | 'Organization' | 'LocalBusiness';
  data: Record<string, any>;
}

// ============================================================
// SEO META TAGS COMPONENT
// ============================================================

interface SEOMetaTagsProps {
  metadata: SEOMetadata;
  url?: string;
}

export const SEOMetaTags: React.FC<SEOMetaTagsProps> = memo(({ metadata, url }) => {
  const {
    title,
    description,
    keywords,
    ogTitle,
    ogDescription,
    ogImage,
    twitterTitle,
    twitterDescription,
    twitterImage,
    canonicalUrl,
    noIndex,
    noFollow,
  } = metadata;

  return (
    <Helmet>
      {/* Primary Meta Tags */}
      <title>{title}</title>
      <meta name="description" content={description} />
      <meta name="keywords" content={keywords} />

      {/* Canonical URL */}
      {canonicalUrl && <link rel="canonical" href={canonicalUrl} />}

      {/* Robots Meta Tags */}
      {(noIndex || noFollow) && (
        <meta
          name="robots"
          content={`${noIndex ? 'noindex' : ''} ${noFollow ? 'nofollow' : ''}`.trim()}
        />
      )}

      {/* Open Graph / Facebook */}
      <meta property="og:type" content="website" />
      <meta property="og:title" content={ogTitle || title} />
      <meta property="og:description" content={ogDescription || description} />
      {url && <meta property="og:url" content={url} />}
      {ogImage && <meta property="og:image" content={ogImage} />}

      {/* Twitter Card */}
      <meta name="twitter:card" content="summary_large_image" />
      <meta name="twitter:title" content={twitterTitle || title} />
      <meta name="twitter:description" content={twitterDescription || description} />
      {twitterImage && <meta name="twitter:image" content={twitterImage} />}

      {/* Additional Meta Tags */}
      <meta name="viewport" content="width=device-width, initial-scale=1" />
      <meta charSet="UTF-8" />
    </Helmet>
  );
});

SEOMetaTags.displayName = 'SEOMetaTags';

// ============================================================
// STRUCTURED DATA COMPONENT
// ============================================================

interface StructuredDataProps {
  data: StructuredData;
}

export const StructuredData: React.FC<StructuredDataProps> = memo(({ data }) => {
  const jsonLd = {
    '@context': 'https://schema.org',
    ...data.data,
  };

  return (
    <Helmet>
      <script type="application/ld+json">{JSON.stringify(jsonLd)}</script>
    </Helmet>
  );
});

StructuredData.displayName = 'StructuredData';

// ============================================================
// SEO EDITOR COMPONENT
// ============================================================

interface SEOEditorProps {
  metadata: SEOMetadata;
  onChange: (metadata: SEOMetadata) => void;
  url?: string;
}

export const SEOEditor: React.FC<SEOEditorProps> = memo(({ metadata, onChange, url }) => {
  const handleChange = (field: keyof SEOMetadata, value: any) => {
    onChange({
      ...metadata,
      [field]: value,
    });
  };

  return (
    <Paper sx={{ p: 3 }}>
      <Typography variant="h6" gutterBottom>
        SEO & Metadata
      </Typography>

      <Grid container spacing={2}>
        {/* Basic Meta Tags */}
        <Grid item xs={12}>
          <TextField
            fullWidth
            label="Page Title"
            value={metadata.title}
            onChange={(e) => handleChange('title', e.target.value)}
            helperText="Recommended: 50-60 characters"
            inputProps={{ maxLength: 60 }}
          />
        </Grid>

        <Grid item xs={12}>
          <TextField
            fullWidth
            multiline
            rows={3}
            label="Meta Description"
            value={metadata.description}
            onChange={(e) => handleChange('description', e.target.value)}
            helperText="Recommended: 150-160 characters"
            inputProps={{ maxLength: 160 }}
          />
        </Grid>

        <Grid item xs={12}>
          <TextField
            fullWidth
            label="Keywords"
            value={metadata.keywords}
            onChange={(e) => handleChange('keywords', e.target.value)}
            helperText="Comma-separated keywords"
            placeholder="keyword1, keyword2, keyword3"
          />
        </Grid>

        <Divider sx={{ my: 2, width: '100%' }} />

        {/* Open Graph */}
        <Grid item xs={12}>
          <Typography variant="subtitle2" gutterBottom>
            Open Graph (Facebook/LinkedIn)
          </Typography>
        </Grid>

        <Grid item xs={12}>
          <TextField
            fullWidth
            label="OG Title"
            value={metadata.ogTitle || ''}
            onChange={(e) => handleChange('ogTitle', e.target.value)}
            helperText="Leave empty to use page title"
          />
        </Grid>

        <Grid item xs={12}>
          <TextField
            fullWidth
            multiline
            rows={2}
            label="OG Description"
            value={metadata.ogDescription || ''}
            onChange={(e) => handleChange('ogDescription', e.target.value)}
            helperText="Leave empty to use meta description"
          />
        </Grid>

        <Grid item xs={12}>
          <TextField
            fullWidth
            label="OG Image URL"
            value={metadata.ogImage || ''}
            onChange={(e) => handleChange('ogImage', e.target.value)}
            helperText="Recommended: 1200x630px, <5MB"
            placeholder="https://example.com/og-image.jpg"
          />
        </Grid>

        <Divider sx={{ my: 2, width: '100%' }} />

        {/* Twitter Card */}
        <Grid item xs={12}>
          <Typography variant="subtitle2" gutterBottom>
            Twitter Card
          </Typography>
        </Grid>

        <Grid item xs={12}>
          <TextField
            fullWidth
            label="Twitter Title"
            value={metadata.twitterTitle || ''}
            onChange={(e) => handleChange('twitterTitle', e.target.value)}
            helperText="Leave empty to use page title"
          />
        </Grid>

        <Grid item xs={12}>
          <TextField
            fullWidth
            multiline
            rows={2}
            label="Twitter Description"
            value={metadata.twitterDescription || ''}
            onChange={(e) => handleChange('twitterDescription', e.target.value)}
            helperText="Leave empty to use meta description"
          />
        </Grid>

        <Grid item xs={12}>
          <TextField
            fullWidth
            label="Twitter Image URL"
            value={metadata.twitterImage || ''}
            onChange={(e) => handleChange('twitterImage', e.target.value)}
            helperText="Recommended: 1200x600px, <5MB"
            placeholder="https://example.com/twitter-image.jpg"
          />
        </Grid>

        <Divider sx={{ my: 2, width: '100%' }} />

        {/* Advanced Settings */}
        <Grid item xs={12}>
          <Typography variant="subtitle2" gutterBottom>
            Advanced Settings
          </Typography>
        </Grid>

        <Grid item xs={12}>
          <TextField
            fullWidth
            label="Canonical URL"
            value={metadata.canonicalUrl || ''}
            onChange={(e) => handleChange('canonicalUrl', e.target.value)}
            helperText="Preferred URL for search engines"
            placeholder="https://example.com/page"
          />
        </Grid>

        <Grid item xs={12}>
          <FormControlLabel
            control={
              <Switch
                checked={metadata.noIndex || false}
                onChange={(e) => handleChange('noIndex', e.target.checked)}
              />
            }
            label="No Index (prevent search engine indexing)"
          />
        </Grid>

        <Grid item xs={12}>
          <FormControlLabel
            control={
              <Switch
                checked={metadata.noFollow || false}
                onChange={(e) => handleChange('noFollow', e.target.checked)}
              />
            }
            label="No Follow (prevent link juice)"
          />
        </Grid>

        {/* Preview URL */}
        {url && (
          <Grid item xs={12}>
            <Box sx={{ mt: 2, p: 2, bgcolor: 'action.hover', borderRadius: 1 }}>
              <Typography variant="caption" color="text.secondary">
                Page URL:
              </Typography>
              <Typography variant="body2" sx={{ wordBreak: 'break-all' }}>
                {url}
              </Typography>
            </Box>
          </Grid>
        )}
      </Grid>
    </Paper>
  );
});

SEOEditor.displayName = 'SEOEditor';

// ============================================================
// SEO UTILITIES
// ============================================================

/**
 * Generate default SEO metadata from page content
 */
export function generateDefaultMetadata(pageTitle: string, pageDescription?: string): SEOMetadata {
  return {
    title: pageTitle,
    description: pageDescription || `Learn more about ${pageTitle}`,
    keywords: `${pageTitle}, beyondcode, cms`.toLowerCase(),
    ogTitle: pageTitle,
    ogDescription: pageDescription || `Discover ${pageTitle} on BeyondCode CMS`,
    noIndex: false,
    noFollow: false,
  };
}

/**
 * Generate structured data for organization
 */
export function generateOrganizationStructuredData(orgName: string, url: string, logo?: string): StructuredData {
  return {
    type: 'Organization',
    data: {
      '@type': 'Organization',
      name: orgName,
      url: url,
      logo: logo,
      sameAs: [
        'https://twitter.com/beyondcode',
        'https://linkedin.com/company/beyondcode',
        'https://github.com/beyondcode',
      ],
    },
  };
}

/**
 * Generate structured data for webpage
 */
export function generateWebPageStructuredData(
  title: string,
  description: string,
  url: string,
  datePublished?: string,
  dateModified?: string
): StructuredData {
  return {
    type: 'WebPage',
    data: {
      '@type': 'WebPage',
      name: title,
      description: description,
      url: url,
      datePublished: datePublished,
      dateModified: dateModified,
      inLanguage: 'en-US',
      isPartOf: {
        '@type': 'WebSite',
        name: 'BeyondCode CMS',
        url: 'https://example.com',
      },
    },
  };
}

export default SEOMetaTags;

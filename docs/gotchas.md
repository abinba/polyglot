# Polyglot Gotchas

This document outlines common issues, edge cases, and important considerations when working with or using the Polyglot application.

## API Limitations

### OpenAI Rate Limits
- **Issue**: OpenAI API has rate limits that can be reached during heavy usage
- **Solution**: Implement exponential backoff retry logic in API calls
- **Workaround**: Cache generated vocabulary to reduce API calls

### API Costs
- **Issue**: OpenAI API usage incurs costs based on token usage
- **Solution**: Optimize prompts to reduce token count
- **Workaround**: Generate words in batches rather than individually

## Data Management

### First-Time Initialization
- **Issue**: Application needs special handling for first-time users with no data files
- **Solution**: Check for existence of data files and create with defaults if not found
- **Edge Case**: Ensure directory exists before attempting to create files

### Data Migration
- **Issue**: Updates to data schemas require migration of existing user data
- **Solution**: Implement version-checking and migration logic
- **Workaround**: For major changes, provide a way to reset data with user consent

### Large Vocabulary Sets
- **Issue**: Performance degradation with very large vocabulary sets
- **Solution**: Implement pagination and lazy loading
- **Edge Case**: Test with vocabulary sets >1000 words to ensure performance

## UI Considerations

### Custom Tkinter Quirks
- **Issue**: customtkinter widgets sometimes behave differently than standard tkinter
- **Solution**: Test all UI interactions thoroughly
- **Gotcha**: Some customtkinter features depend on specific Python versions

### Window Resizing
- **Issue**: UI layout can break when window is resized to extreme dimensions
- **Solution**: Set minimum window size and test resize behavior
- **Workaround**: Use pack/grid with appropriate fill and expand options

### Focus Management
- **Issue**: Tab navigation between fields can be inconsistent
- **Solution**: Explicitly manage focus order where needed
- **Edge Case**: Ensure keyboard shortcuts work when different elements have focus

## Learning Algorithm

### Empty Test Sets
- **Issue**: Tests cannot run if no words are available
- **Solution**: Check for empty data frames and show appropriate messages
- **Edge Case**: Handle case where user tries to test before learning any words

### Word Difficulty Estimation
- **Issue**: Word difficulty doesn't always match user's actual experience
- **Solution**: Allow users to manually adjust difficulty level
- **Workaround**: Provide generous thresholds for learning criteria

### Similar Words Confusion
- **Issue**: Similar words or homonyms can be confusing in tests
- **Solution**: Avoid including similar words in the same test session
- **Edge Case**: Consider TTS pronunciation aids for confusable words

## Language Support

### Script Rendering
- **Issue**: Some languages with non-Latin scripts may not display correctly
- **Solution**: Ensure font support for all target languages
- **Edge Case**: Right-to-left languages need special layout considerations

### Special Characters
- **Issue**: Special characters in some languages can cause display or search issues
- **Solution**: Use Unicode-aware string operations
- **Gotcha**: Be careful with case normalization in non-Latin scripts

## Environment-Specific Issues

### API Key Security
- **Issue**: API keys in environment variables can be exposed
- **Solution**: Use a secure credential manager or encrypted storage
- **Workaround**: Prompt for API key on startup rather than storing it

### Cross-Platform Paths
- **Issue**: File paths differ between operating systems
- **Solution**: Use `os.path` or `pathlib` for path operations
- **Gotcha**: Always use `os.path.join()` rather than string concatenation

### Unicode Support
- **Issue**: Windows terminals may have issues with Unicode output
- **Solution**: Configure appropriate code pages or use GUI exclusively
- **Edge Case**: Test on all target platforms with various language inputs

## Troubleshooting

### Common Errors

1. **"No such file or directory"**
   - Likely cause: Application data directory doesn't exist
   - Solution: Create directory structure before accessing files

2. **"API key not found"**
   - Likely cause: Missing or invalid OpenAI API key
   - Solution: Check `.env` file or environment variables

3. **"No words available for testing"**
   - Likely cause: User hasn't reviewed any words in flashcard view
   - Solution: Direct user to first complete flashcard review

4. **"Unable to generate word details"**
   - Likely cause: OpenAI API error or rate limiting
   - Solution: Implement retry logic and provide meaningful error messages

## Known Limitations

- Maximum vocabulary size is currently unlimited but performance degrades with very large sets
- Offline mode is not supported - internet connection required for word generation
- No audio pronunciation support for vocabulary words
- Limited support for grammatical variations of words

## Next Steps

For quick reference of key parameters and configurations, see [Quick Reference](quick_reference.md).

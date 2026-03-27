# Propact Examples Makefile
# Convenient targets for running and testing examples

.PHONY: help test test-offline test-online test-core test-popular test-legacy test-all clean install deps list dry-run

# Default target
help:
	@echo "Propact Examples - Available targets:"
	@echo ""
	@echo "Testing:"
	@echo "  test-offline    Run offline examples (no API keys required)"
	@echo "  test-online     Run online examples (requires API keys)"
	@echo "  test-core       Run core examples (01-08)"
	@echo "  test-popular    Run popular services examples (09-17)"
	@echo "  test-legacy     Run legacy examples"
	@echo "  test-all        Run all examples"
	@echo "  dry-run         Validate all examples without executing"
	@echo ""
	@echo "Utilities:"
	@echo "  list            List all available examples"
	@echo "  clean           Clean up generated files"
	@echo "  install         Install propact in development mode"
	@echo "  deps            Install all optional dependencies"
	@echo ""
	@echo "Individual examples:"
	@echo "  01, 02, ... 17  Run specific example"
	@echo ""
	@echo "Examples with environment variables:"
	@echo "  check-env       Check which environment variables are set"

# Installation
install:
	@echo "Installing propact in development mode..."
	pip install -e ..

deps:
	@echo "Installing all optional dependencies..."
	pip install -e ..[all]

# Testing targets
test-offline:
	@echo "Running offline examples..."
	./run-all.sh --offline

test-online:
	@echo "Running online examples (requires API keys)..."
	./run-all.sh --online

test-core:
	@echo "Running core examples (01-08)..."
	./run-all.sh --category core

test-popular:
	@echo "Running popular services examples (09-17)..."
	./run-all.sh --category popular --online

test-legacy:
	@echo "Running legacy examples..."
	./run-all.sh --category legacy

test-all:
	@echo "Running all examples..."
	./run-all.sh

# Validation
dry-run:
	@echo "Validating all examples without execution..."
	./run-all.sh --dry-run

# Environment checking
check-env:
	@echo "Checking environment variables..."
	@echo ""
	@for dir in */; do \
		if [ -f "$$dir/.env" ]; then \
			echo "$$dir.env:"; \
			while IFS= read -r line; do \
				if [[ $$line =~ ^[A-Z_]+= ]]; then \
					var=$${line%%=*}; \
					if [ -z "$${!var}" ]; then \
						echo "  ❌ $$var is not set"; \
					else \
						echo "  ✅ $$var is set"; \
					fi; \
				fi; \
			done < "$$dir/.env"; \
			echo ""; \
		fi; \
	done

# List examples
list:
	@echo "Available examples:"
	@echo ""
	@echo "Core Examples (01-08):"
	@for i in 01 02 03 04 05 06 07 08; do \
		if [ -d "$$i"-* ]; then \
			name=$$(basename "$$i"-*); \
			if [ -f "$$name/.env" ]; then \
				echo "  $$name - requires API keys"; \
			else \
				echo "  $$name - offline"; \
			fi; \
		fi; \
	done
	@echo ""
	@echo "Popular Services (09-17):"
	@for i in 09 10 11 12 13 14 15 16 17; do \
		if [ -d "$$i"-* ]; then \
			name=$$(basename "$$i"-*); \
			echo "  $$name - requires API keys"; \
		fi; \
	done
	@echo ""
	@echo "Legacy Examples:"
	@for dir in shell-to-mcp rest-ws-proxy; do \
		if [ -d "$$dir" ]; then \
			echo "  $$dir/"; \
		fi; \
	done

# Individual example targets
01:
	@cd 01-shell-upload && ./run.sh

02:
	@cd 02-openapi-rest && ./run.sh

03:
	@cd 03-mcp-tool && ./run.sh

04:
	@cd 04-ws-chat && ./run.sh

05:
	@cd 05-md-server && ./run.sh

06:
	@echo "Note: 06-openai-vision requires OPENAI_API_KEY"
	@cd 06-openai-vision && ./run.sh

07:
	@cd 07-ffmpeg-cli && ./run.sh

08:
	@cd 08-grpc-inference && ./run.sh

09:
	@echo "Note: 09-imgur requires IMGUR_CLIENT_ID"
	@cd 09-imgur && ./run.sh

10:
	@echo "Note: 10-slack requires SLACK_TOKEN"
	@cd 10-slack && ./run.sh

11:
	@echo "Note: 11-discord requires DISCORD_TOKEN and DISCORD_CHANNEL_ID"
	@cd 11-discord && ./run.sh

12:
	@echo "Note: 12-openai-vision requires OPENAI_API_KEY"
	@cd 12-openai-vision && ./run.sh

13:
	@echo "Note: 13-github-gist requires GITHUB_TOKEN"
	@cd 13-github-gist && ./run.sh

14:
	@echo "Note: 14-stripe requires STRIPE_SECRET_KEY"
	@cd 14-stripe && ./run.sh

15:
	@echo "Note: 15-youtube requires YOUTUBE_ACCESS_TOKEN"
	@cd 15-youtube && ./run.sh

16:
	@echo "Note: 16-notion requires NOTION_TOKEN"
	@cd 16-notion && ./run.sh

17:
	@echo "Note: 17-twitter requires TWITTER_BEARER"
	@cd 17-twitter && ./run.sh

# Clean up generated files
clean:
	@echo "Cleaning up generated files..."
	@find . -name "*.response.md" -delete
	@find . -name "*.temp.*" -delete
	@find . -name "*.tmp.*" -delete
	@find . -name ".DS_Store" -delete
	@find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true
	@echo "Clean complete"

# Make scripts executable
chmod:
	@echo "Making all scripts executable..."
	@chmod +x */run.sh
	@for dir in shell-to-mcp rest-ws-proxy; do \
		if [ -f "$$dir/run.sh" ]; then \
			chmod +x "$$dir/run.sh"; \
		fi; \
	done
	@echo "Done"

ADR_SOURCE = decision-records


adr:
	@read -p "Enter the file name: " NAME; \
	DATE=$$(date +%Y-%m-%d); \
	FILE_NAME="${ADR_SOURCE}/$${DATE}_$${NAME}.md"; \
	sed "s/{{ name }}/$${NAME}/g; s/{{ date }}/$${DATE}/g" "${ADR_SOURCE}/template.md" > "$$FILE_NAME"; \
	echo "Generated file: $${FILE_NAME}"

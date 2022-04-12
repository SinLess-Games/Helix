package com.sinlessgamesllc.web.rest;

import com.sinlessgamesllc.domain.Deals;
import com.sinlessgamesllc.repository.DealsRepository;
import com.sinlessgamesllc.service.DealsService;
import com.sinlessgamesllc.web.rest.errors.BadRequestAlertException;
import java.net.URI;
import java.net.URISyntaxException;
import java.util.List;
import java.util.Objects;
import java.util.Optional;
import javax.validation.Valid;
import javax.validation.constraints.NotNull;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import tech.jhipster.web.util.HeaderUtil;
import tech.jhipster.web.util.ResponseUtil;

/**
 * REST controller for managing {@link com.sinlessgamesllc.domain.Deals}.
 */
@RestController
@RequestMapping("/api")
public class DealsResource {

    private final Logger log = LoggerFactory.getLogger(DealsResource.class);

    private static final String ENTITY_NAME = "invoiceDeals";

    @Value("${jhipster.clientApp.name}")
    private String applicationName;

    private final DealsService dealsService;

    private final DealsRepository dealsRepository;

    public DealsResource(DealsService dealsService, DealsRepository dealsRepository) {
        this.dealsService = dealsService;
        this.dealsRepository = dealsRepository;
    }

    /**
     * {@code POST  /deals} : Create a new deals.
     *
     * @param deals the deals to create.
     * @return the {@link ResponseEntity} with status {@code 201 (Created)} and with body the new deals, or with status {@code 400 (Bad Request)} if the deals has already an ID.
     * @throws URISyntaxException if the Location URI syntax is incorrect.
     */
    @PostMapping("/deals")
    public ResponseEntity<Deals> createDeals(@Valid @RequestBody Deals deals) throws URISyntaxException {
        log.debug("REST request to save Deals : {}", deals);
        if (deals.getId() != null) {
            throw new BadRequestAlertException("A new deals cannot already have an ID", ENTITY_NAME, "idexists");
        }
        Deals result = dealsService.save(deals);
        return ResponseEntity
            .created(new URI("/api/deals/" + result.getId()))
            .headers(HeaderUtil.createEntityCreationAlert(applicationName, true, ENTITY_NAME, result.getId().toString()))
            .body(result);
    }

    /**
     * {@code PUT  /deals/:id} : Updates an existing deals.
     *
     * @param id the id of the deals to save.
     * @param deals the deals to update.
     * @return the {@link ResponseEntity} with status {@code 200 (OK)} and with body the updated deals,
     * or with status {@code 400 (Bad Request)} if the deals is not valid,
     * or with status {@code 500 (Internal Server Error)} if the deals couldn't be updated.
     * @throws URISyntaxException if the Location URI syntax is incorrect.
     */
    @PutMapping("/deals/{id}")
    public ResponseEntity<Deals> updateDeals(@PathVariable(value = "id", required = false) final Long id, @Valid @RequestBody Deals deals)
        throws URISyntaxException {
        log.debug("REST request to update Deals : {}, {}", id, deals);
        if (deals.getId() == null) {
            throw new BadRequestAlertException("Invalid id", ENTITY_NAME, "idnull");
        }
        if (!Objects.equals(id, deals.getId())) {
            throw new BadRequestAlertException("Invalid ID", ENTITY_NAME, "idinvalid");
        }

        if (!dealsRepository.existsById(id)) {
            throw new BadRequestAlertException("Entity not found", ENTITY_NAME, "idnotfound");
        }

        Deals result = dealsService.save(deals);
        return ResponseEntity
            .ok()
            .headers(HeaderUtil.createEntityUpdateAlert(applicationName, true, ENTITY_NAME, deals.getId().toString()))
            .body(result);
    }

    /**
     * {@code PATCH  /deals/:id} : Partial updates given fields of an existing deals, field will ignore if it is null
     *
     * @param id the id of the deals to save.
     * @param deals the deals to update.
     * @return the {@link ResponseEntity} with status {@code 200 (OK)} and with body the updated deals,
     * or with status {@code 400 (Bad Request)} if the deals is not valid,
     * or with status {@code 404 (Not Found)} if the deals is not found,
     * or with status {@code 500 (Internal Server Error)} if the deals couldn't be updated.
     * @throws URISyntaxException if the Location URI syntax is incorrect.
     */
    @PatchMapping(value = "/deals/{id}", consumes = { "application/json", "application/merge-patch+json" })
    public ResponseEntity<Deals> partialUpdateDeals(
        @PathVariable(value = "id", required = false) final Long id,
        @NotNull @RequestBody Deals deals
    ) throws URISyntaxException {
        log.debug("REST request to partial update Deals partially : {}, {}", id, deals);
        if (deals.getId() == null) {
            throw new BadRequestAlertException("Invalid id", ENTITY_NAME, "idnull");
        }
        if (!Objects.equals(id, deals.getId())) {
            throw new BadRequestAlertException("Invalid ID", ENTITY_NAME, "idinvalid");
        }

        if (!dealsRepository.existsById(id)) {
            throw new BadRequestAlertException("Entity not found", ENTITY_NAME, "idnotfound");
        }

        Optional<Deals> result = dealsService.partialUpdate(deals);

        return ResponseUtil.wrapOrNotFound(
            result,
            HeaderUtil.createEntityUpdateAlert(applicationName, true, ENTITY_NAME, deals.getId().toString())
        );
    }

    /**
     * {@code GET  /deals} : get all the deals.
     *
     * @return the {@link ResponseEntity} with status {@code 200 (OK)} and the list of deals in body.
     */
    @GetMapping("/deals")
    public List<Deals> getAllDeals() {
        log.debug("REST request to get all Deals");
        return dealsService.findAll();
    }

    /**
     * {@code GET  /deals/:id} : get the "id" deals.
     *
     * @param id the id of the deals to retrieve.
     * @return the {@link ResponseEntity} with status {@code 200 (OK)} and with body the deals, or with status {@code 404 (Not Found)}.
     */
    @GetMapping("/deals/{id}")
    public ResponseEntity<Deals> getDeals(@PathVariable Long id) {
        log.debug("REST request to get Deals : {}", id);
        Optional<Deals> deals = dealsService.findOne(id);
        return ResponseUtil.wrapOrNotFound(deals);
    }

    /**
     * {@code DELETE  /deals/:id} : delete the "id" deals.
     *
     * @param id the id of the deals to delete.
     * @return the {@link ResponseEntity} with status {@code 204 (NO_CONTENT)}.
     */
    @DeleteMapping("/deals/{id}")
    public ResponseEntity<Void> deleteDeals(@PathVariable Long id) {
        log.debug("REST request to delete Deals : {}", id);
        dealsService.delete(id);
        return ResponseEntity
            .noContent()
            .headers(HeaderUtil.createEntityDeletionAlert(applicationName, true, ENTITY_NAME, id.toString()))
            .build();
    }
}
